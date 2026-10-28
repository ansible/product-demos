# OpenFlake — ITSM on OpenShift

Deploy [OpenFlake](https://github.com/rlopez133/open-flake) — a lightweight ITSM platform with a ServiceNow-compatible REST API — on an OpenShift cluster. It gives demos a real incident/change backend to drive without needing a ServiceNow instance, and the ServiceNow-compatible endpoints mean `servicenow.itsm` content can point at it with only a URL change.

This is **not** part of the automatic `infrastructure` demo setup. The job template is seeded by the demo setup, but the deployment only happens when someone launches it.

## Prerequisites

- OpenShift cluster with privileges to create projects, deployments, statefulsets, services, routes and PVCs
- A default StorageClass, or a StorageClass name to pass in (two PVCs are created: 10Gi for Postgres, 5Gi for attachments)
- OpenShift Credential configured in AAP (bearer token for cluster authentication)
- Product Demos EE, or another EE with `helm` on PATH — see [Helm binary](#helm-binary)

## Configure credentials

| Credential | Type | Where to get it |
|------------|------|-----------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | OpenShift console — Service Account or user token |

## Survey prompts

| Prompt | Variable | Type | Required | Default |
|--------|----------|------|----------|---------|
| Operation | `openflake_operation` | multiplechoice (`install` / `uninstall`) | Yes | `install` |
| OpenFlake namespace | `openflake_namespace` | text | Yes | `openflake` |
| Route hostname | `openflake_route_host` | text | No | *(blank — OpenShift generates one)* |
| OpenFlake image tag | `openflake_image_tag` | text | Yes | `stable` |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Infrastructure ǀ OpenFlake | [`infrastructure/openflake/provision.yml`](../openflake/provision.yml) | Installs or removes OpenFlake via the bundled Helm chart |

## What gets deployed

| Component | Kind | Notes |
|-----------|------|-------|
| `openflake-backend` | Deployment | FastAPI app serving the ServiceNow-compatible REST API; Alembic migrations run on startup |
| `openflake-frontend` | Deployment | nginx serving the UI and proxying `/api` to the backend |
| `openflake-postgresql` | StatefulSet | Postgres 16 (`quay.io/sclorg/postgresql-16-c9s`) |
| `openflake` | Route | Edge TLS with HTTP redirect |
| `openflake` | Secret | Admin password, JWT signing key, Postgres password |

## Credentials

Leave the admin password unset (the default) and the chart generates one on first install, then reuses it on every subsequent run via a cluster lookup — re-running the template will not roll the password out from under a running demo.

The job output prints the URL, username and password at the end of a successful install, so they can be copied straight out of the job.

> [!NOTE]
> That is a deliberate choice for a demo workload: AAP retains job output and shows it to anyone with read access on the job. Fine for an ephemeral demo cluster, not something to carry into anything long-lived. Only the admin password is exposed — the same Secret also holds `SECRET_KEY` and `POSTGRESQL_PASSWORD`, and those stay out of the log.

The password is also readable from the Secret at any time:

```bash
oc -n openflake get secret openflake -o jsonpath="{.data.ADMIN_PASSWORD}" | base64 -d
```

Override with `openflake_admin_username` / `openflake_admin_password` in extra_vars if you need a fixed login.

## Route hostname

Leaving **Route hostname** blank is the normal path. The chart installs with `BASE_URL`/`CORS_ORIGINS` pointed at the in-cluster Service, the playbook then reads back the hostname OpenShift generated and runs a second Helm pass to correct them. Helm is idempotent, so later runs converge to a no-op.

Supplying a hostname skips the second pass.

## Helm binary

`kubernetes.core.helm` shells out to the `helm` CLI. Product Demos EE already bakes it into `/usr/local/bin/helm` — see the `append_final` step in [`execution_environments/apd-ee-27.yml`](../../execution_environments/apd-ee-27.yml) (same in the `apd-ee-25` and `apd-ee-26` definitions). The template does not set an execution environment, so it runs on Product Demos EE as the organization default and helm is on PATH.

Preflight fails with a clear message if it is not. To run on an EE that ships helm somewhere else:

```yaml
openflake_helm_binary: /usr/bin/helm
```

Note the EE installs the `linux-amd64` build, so the job needs an amd64 execution node.

## Uninstall

Set **Operation** to `uninstall`. The playbook removes the Helm release, waits for the pods to finish terminating, then deletes the namespace — which takes the PVCs with it. **This destroys all OpenFlake data.**

Before deleting anything it checks that the namespace actually holds resources labelled `app.kubernetes.io/part-of=openflake` for this release, and aborts if it does not. A mistyped namespace fails the job rather than deleting an unrelated project. The same check means uninstalling an already-removed release fails too — that is deliberate.

To keep the namespace and only drop the release and its claims:

```yaml
openflake_remove_namespace: false
openflake_remove_pvcs: true
```

## Extra variables

Everything the survey does not expose is settable in extra_vars.

| Variable | Default | Purpose |
|----------|---------|---------|
| `openflake_release_name` | `openflake` | Helm release name |
| `openflake_image_registry` | `quay.io/rlopez133/openflake` | Registry and org holding the images |
| `openflake_image_pull_policy` | `Always` | `stable` is a mutable tag, so `IfNotPresent` would reuse a stale layer |
| `openflake_route_enabled` | `true` | Set false for in-cluster-only access |
| `openflake_route_tls_enabled` | `true` | Edge TLS termination |
| `openflake_admin_username` | `admin` | Seed admin username |
| `openflake_admin_password` | *(generated)* | Pin the admin password instead of letting the chart generate it |
| `openflake_storage_class` | *(cluster default)* | StorageClass for both PVCs |
| `openflake_postgres_storage_size` | `10Gi` | Postgres volume |
| `openflake_attachments_storage_size` | `5Gi` | Attachments volume |
| `openflake_wait_timeout` | `10m` | Helm wait timeout |
| `openflake_verify` | `true` | Wait for Postgres, backend and frontend to report ready |
| `openflake_validate_certs` | *(from the credential's `K8S_AUTH_VERIFY_SSL`)* | Verify the cluster API certificate when helm connects |
| `openflake_ca_cert` | *(from the credential's `K8S_AUTH_SSL_CA_CERT`)* | Cluster CA for helm — a file path, or an inline PEM the playbook spills to a temp file |
| `openflake_helm_binary` | *(PATH lookup)* | Absolute path to helm on EEs that do not put it on PATH |

## Known issues

- The chart is vendored at [`infrastructure/openflake/chart`](../openflake/chart) rather than pulled from a chart repository, so it does not pick up upstream chart changes automatically. Update it in place when OpenFlake ships a new chart version.
- First boot can take several minutes: Alembic migrations run behind a Postgres advisory lock before the backend passes its startup probe.
- The deployment is not hardened for production — it is a demo backend.

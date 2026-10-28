# OpenFlake — ITSM on OpenShift

Deploy [OpenFlake](https://github.com/rlopez133/open-flake) — a lightweight ITSM platform with a ServiceNow-compatible REST API — on an OpenShift cluster. It gives demos a real incident/change backend to drive without needing a ServiceNow instance, and the ServiceNow-compatible endpoints mean `servicenow.itsm` content can point at it with only a URL change.

This is **not** part of the automatic `infrastructure` demo setup. The job template is seeded by the demo setup, but the deployment only happens when someone launches it.

## Prerequisites

- OpenShift cluster with privileges to create projects, deployments, statefulsets, services, routes and PVCs
- A default StorageClass, or a StorageClass name to pass in (two PVCs are created: 10Gi for Postgres, 5Gi for attachments)
- OpenShift Credential configured in AAP (bearer token for cluster authentication)
- Egress from the execution node to `get.helm.sh` — see [Helm binary](#helm-binary)

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
| Infrastructure ǀ OpenShift - Provision OpenFlake | [`infrastructure/openflake/provision.yml`](../openflake/provision.yml) | Installs or removes OpenFlake via the bundled Helm chart |

## What gets deployed

| Component | Kind | Notes |
|-----------|------|-------|
| `openflake-backend` | Deployment | FastAPI app serving the ServiceNow-compatible REST API; Alembic migrations run on startup |
| `openflake-frontend` | Deployment | nginx serving the UI and proxying `/api` to the backend |
| `openflake-postgresql` | StatefulSet | Postgres 16 (`quay.io/sclorg/postgresql-16-c9s`) |
| `openflake` | Route | Edge TLS with HTTP redirect |
| `openflake` | Secret | Admin password, JWT signing key, Postgres password |

## Credentials

Leave the admin password unset (the default) and the chart generates one on first install, then reuses it on every subsequent run via a cluster lookup — re-running the template will not roll the password out from under a running demo. The job output prints the URL, username and password at the end of a successful install; they are also readable from the `openflake` Secret in the namespace.

Override with `openflake_admin_username` / `openflake_admin_password` in extra_vars if you need a fixed login.

## Route hostname

Leaving **Route hostname** blank is the normal path. The chart installs with `BASE_URL`/`CORS_ORIGINS` pointed at the in-cluster Service, the playbook then reads back the hostname OpenShift generated and runs a second Helm pass to correct them. Helm is idempotent, so later runs converge to a no-op.

Supplying a hostname skips the second pass.

## Helm binary

`kubernetes.core.helm` shells out to the `helm` CLI, which the Product Demos EE does not ship. The playbook downloads helm (checksum-verified) to `/tmp/openflake-helm` on every run, so the execution node needs egress to `get.helm.sh`.

If that egress is not available, build helm into your EE and point the playbook at it:

```yaml
openflake_helm_binary: /usr/bin/helm
```

## Uninstall

Set **Operation** to `uninstall`. The playbook removes the Helm release, waits for the pods to finish terminating, then deletes the namespace — which takes the PVCs with it. **This destroys all OpenFlake data.**

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
| `openflake_validate_certs` | `false` | Verify the cluster API certificate |
| `openflake_helm_install_if_missing` | `true` | Download helm when it is not on PATH |

## Known issues

- The chart is vendored at [`infrastructure/openflake/chart`](../openflake/chart) and ported from the `ocp4_workload_openflake` role in the `intro-ao-workshop` repo. Chart changes made there do not flow here automatically.
- First boot can take several minutes: Alembic migrations run behind a Postgres advisory lock before the backend passes its startup probe.
- The deployment is not hardened for production — it is a demo backend.

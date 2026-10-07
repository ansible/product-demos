# Automation Orchestrator — Provisioning

Turn on Automation Orchestrator with one job. On the [Ansible Product Demos catalog item](https://red.ht/apd-sandbox) from [demo.redhat.com](https://demo.redhat.com), OpenShift, credentials, and the AO execution environment are already wired up — launch **Infrastructure ǀ Automation Orchestrator ǀ Install**, wait for it to finish, and use the URL and admin password from the job output.

Under the hood the playbook runs `aapctl`, stands up CloudNativePG plus the AO operator, allow-lists the AAP gateway, wires an AAP integration inside AO, and seeds curated demo workflows from [`infrastructure/ao/demos.yml`](../ao/demos.yml) so AO does not boot empty.

## Prerequisites

- **If using RHDP (demo.redhat.com):** OpenShift, the **OpenShift Credential**, the **AAP Credential**, and the **AO Execution Environment** ship with the catalog item. Run **APD ǀ Multi-demo setup** (or **APD ǀ Single demo setup** → `infrastructure`) if the AO templates are not visible yet.
- **Recommended before running the disk demo:** **Deploy Cloud Stack in AWS** so `aws_rhel9` is in inventory (Install warns if it is missing, but still seeds the workflow)
- **Recommended:** **Infrastructure ǀ AWS - Provision Mattermost** so Notify Chatroom can post (see [Mattermost](./mattermost.md))
- **If using your own installation:** You need an OpenShift cluster, OpenShift + AAP credentials in AAP, the AO EE (`quay.io/acme_corp/ao-ee:latest`), and **APD ǀ Single demo setup** with category `infrastructure`.

## Configure credentials

| Credential | Type | On demo.redhat.com |
|------------|------|--------------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | Pre-configured |
| AAP Credential | Red Hat Ansible Automation Platform | Pre-configured |

Only set these yourself if you are running APD outside RHDP.

## Survey prompts

No surveys. Click Launch on Install — defaults are fine.

| Template | Variable | Default | When to change it |
|----------|----------|---------|-------------------|
| Install | `ao_operator_channel` | `stable` | Rarely — only if you need a non-stable operator channel |
| Network Configuration | `aap_hostname` / `ao_extra_hosts` | from AAP credential | Only if you re-run network config with overrides |
| Uninstall | — | — | No prompts |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Infrastructure ǀ Automation Orchestrator ǀ Install | [`infrastructure/ao/install.yml`](../ao/install.yml) | `aapctl install ao`, network access, AAP wiring, curated demo seed |
| Infrastructure ǀ AO Network Configuration ǀ Install | [`infrastructure/ao/network-access.yml`](../ao/network-access.yml) | Re-run allow-listing / private-network OIDC if needed (Install already does this) |
| Infrastructure ǀ Automation Orchestrator ǀ Uninstall | [`infrastructure/ao/uninstall.yml`](../ao/uninstall.yml) | Tear down AO when the demo is done |
| Infrastructure ǀ AWS - Provision Mattermost | [`infrastructure/mattermost/provision_mattermost.yml`](../mattermost/provision_mattermost.yml) | Chat backend for demo notifications |

## Curated demos (`demos.yml`)

Install only seeds demos listed with `enabled: true` in [`infrastructure/ao/demos.yml`](../ao/demos.yml). Today that is **disk-utilization** from [aap-orchestrator-demos](https://github.com/ansible-tmm/aap-orchestrator-demos).

On seed, Install:

1. Creates AAP project **AAP Orchestrator Demos** (SCM to the upstream repo) and the demo job templates in org **Ansible Product Demos (APD)** — not declared in `setup.yml`, so they only appear when AO is installed
2. Rewrites workflow JSON `organization_name` from `Default` → **Ansible Product Demos (APD)** and injects the AO AAP credential/integration IDs
3. Imports the selected workflow into AO (idempotent create/update by `source_file` label)

To add another demo later: append a catalog entry and set `enabled: true`.

## Why it matters

- **Demo-ready on RHDP** — Catalog item already has the cluster and credentials; the story is “press Launch,” not “assemble a platform”
- **AO boots with a real workflow** — disk utilization check → switch → remediate → notify, not an empty canvas
- **No JT sprawl** — demo job templates are created at Install time from the catalog, not permanently registered for every APD environment
- **Clean exit** — Uninstall is a first-class template so shared lab clusters do not keep orphaned AO namespaces

## Presenter walkthrough

1. Order the Ansible Product Demos item from [demo.redhat.com](https://red.ht/apd-sandbox) (or open your existing lab)
2. Launch **Deploy Cloud Stack in AWS** and wait for `aws_rhel9` in inventory
3. (Recommended) Launch **Infrastructure ǀ AWS - Provision Mattermost**; copy the bot token from the job output
4. Launch **Infrastructure ǀ Automation Orchestrator ǀ Install** — no survey answers required; it takes several minutes (timeout is 60 minutes)
5. When the job succeeds, open the AO URL from the job output, log in as `admin` with the printed password, and open the seeded disk-utilization workflow
6. When finished, launch **Infrastructure ǀ Automation Orchestrator ǀ Uninstall**

Skip the Network Configuration template unless you changed the AAP gateway or need extra allow-listed hosts — Install already ran it.

## Talking points

- This is the supported path: AAP drives `aapctl`, the same CLI an admin would use
- Seeding reuses the same normalize/import approach as aap-demo, filtered by a YAML allowlist
- Upstream workflow exports say `organization_name: Default`; APD rewrites that to the APD org at import time
- Uninstall keeps the shared demo cluster tidy for the next presenter

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Mattermost](./mattermost.md) | Chat server used by seeded AO notify steps |
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | Provision an OpenShift cluster on AWS when you are not using the RHDP catalog item |
| [OPA — Policy as Code](./opa-policy-as-code.md) | Another OpenShift-backed control-plane component launched from AAP |

# Automation Orchestrator — Provisioning

Turn on Automation Orchestrator with one job. On the [Ansible Product Demos catalog item](https://red.ht/apd-sandbox) from [demo.redhat.com](https://demo.redhat.com), OpenShift, credentials, and the AO execution environment are already wired up — launch **Infrastructure ǀ Automation Orchestrator ǀ Install**, wait for it to finish, and use the URL and admin password from the job output.

Under the hood the playbook runs `aapctl`, stands up CloudNativePG plus the AO operator, and allow-lists the AAP gateway so Controller and Orchestrator can talk. You do not need to do any of that by hand on RHDP.

## Prerequisites

- **If using RHDP (demo.redhat.com):** Nothing extra. OpenShift, the **OpenShift Credential**, the **AAP Credential**, and the **AO Execution Environment** ship with the catalog item. Run **APD ǀ Multi-demo setup** (or **APD ǀ Single demo setup** → `infrastructure`) if the AO templates are not visible yet, then launch Install.
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
| Infrastructure ǀ Automation Orchestrator ǀ Install | [`infrastructure/ao/install.yml`](../ao/install.yml) | One-click deploy: `aapctl install ao`, wait for the Route, print admin URL/password, configure network access |
| Infrastructure ǀ AO Network Configuration ǀ Install | [`infrastructure/ao/network-access.yml`](../ao/network-access.yml) | Re-run allow-listing / private-network OIDC if needed (Install already does this) |
| Infrastructure ǀ Automation Orchestrator ǀ Uninstall | [`infrastructure/ao/uninstall.yml`](../ao/uninstall.yml) | Tear down AO when the demo is done |

## Why it matters

- **Demo-ready on RHDP** — Catalog item already has the cluster and credentials; the story is “press Launch,” not “assemble a platform”
- **Day-0 to day-1 in one job** — Operators, database, and AAP allow-listing finish before the job succeeds
- **Clean exit** — Uninstall is a first-class template so shared lab clusters do not keep orphaned AO namespaces

## Presenter walkthrough

1. Order the Ansible Product Demos item from [demo.redhat.com](https://red.ht/apd-sandbox) (or open your existing lab)
2. Launch **Infrastructure ǀ Automation Orchestrator ǀ Install** — no survey answers required; it takes several minutes (timeout is 60 minutes)
3. When the job succeeds, open the AO URL from the job output and log in as `admin` with the printed password (retry for a minute or two if login fails right after deploy)
4. When finished, launch **Infrastructure ǀ Automation Orchestrator ǀ Uninstall**

Skip the Network Configuration template unless you changed the AAP gateway or need extra allow-listed hosts — Install already ran it.

## Talking points

- This is the supported path: AAP drives `aapctl`, the same CLI an admin would use
- On RHDP the hard parts (OpenShift access, credentials, EE with `aapctl`) are already done — the demo is the install itself
- Network allow-listing is included so AAP and AO can integrate immediately after Install succeeds
- Uninstall keeps the shared demo cluster tidy for the next presenter

## Related demos

| Demo | Description |
|------|-------------|
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | Provision an OpenShift cluster on AWS when you are not using the RHDP catalog item |
| [OPA — Policy as Code](./opa-policy-as-code.md) | Another OpenShift-backed control-plane component launched from AAP |

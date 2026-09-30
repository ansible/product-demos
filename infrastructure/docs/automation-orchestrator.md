# Automation Orchestrator — Provisioning

Deploy Red Hat Automation Orchestrator on an existing OpenShift cluster from AAP. The install job runs `aapctl`, stands up CloudNativePG plus the AO operator, then allow-lists the AAP gateway so Controller and Orchestrator can talk to each other. Uninstall tears the stack down cleanly when the demo is done.

## Prerequisites

- OpenShift cluster with privileges to create namespaces, operators, Deployments, Secrets, and Routes
- **OpenShift Credential** configured in AAP (OpenShift or Kubernetes API Bearer Token)
- **AAP Credential** configured in AAP (gateway URL + credentials — used to build the integration allow-list)
- **AO Execution Environment** available (`quay.io/acme_corp/ao-ee:latest`) — must include `aapctl` and `kubectl`
- **APD ǀ Single demo setup** — category `infrastructure` (creates the AO job templates and EE)

## Configure credentials

| Credential | Type | Where to get it |
|------------|------|-----------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | OpenShift console — Service Account or user token with cluster-admin (or equivalent) |
| AAP Credential | Red Hat Ansible Automation Platform | AAP instance — admin credentials; `CONTROLLER_HOST` must be reachable from AO |

## Survey prompts

These job templates do not use surveys. Install pins the operator channel as an extra var; Network Configuration prompts for extra vars on launch when you need overrides.

### Infrastructure ǀ Automation Orchestrator ǀ Install

| Variable | Type | Default | Notes |
|----------|------|---------|-------|
| `ao_operator_channel` | extra var | `stable` | Operator subscription channel passed to `aapctl install ao` |

### Infrastructure ǀ AO Network Configuration ǀ Install

| Variable | Type | Required | Notes |
|----------|------|----------|-------|
| `aap_hostname` | extra var | No | Override AAP gateway URL if the attached AAP credential does not set `CONTROLLER_HOST` / `AAP_HOSTNAME` |
| `ao_extra_hosts` | extra var | No | Additional hostnames to add to `APP_INTEGRATION_URL_ALLOWED_HOSTS` (list) |

### Infrastructure ǀ Automation Orchestrator ǀ Uninstall

No prompts — attach the OpenShift credential and launch.

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Infrastructure ǀ Automation Orchestrator ǀ Install | [`infrastructure/ao/install.yml`](../ao/install.yml) | Runs `aapctl install ao` (CloudNativePG + AO operator), waits for the Route, prints admin URL/password, then runs network access configuration |
| Infrastructure ǀ AO Network Configuration ǀ Install | [`infrastructure/ao/network-access.yml`](../ao/network-access.yml) | Allow-lists AAP + AO hostnames, enables private-network OIDC, restarts AO Deployments |
| Infrastructure ǀ Automation Orchestrator ǀ Uninstall | [`infrastructure/ao/uninstall.yml`](../ao/uninstall.yml) | Runs `aapctl` uninstall to remove AO, the CloudNativePG cluster, operators, and namespaces |

## Why it matters

- **Day-0 to day-1 in one job** — Operators, database, and network allow-listing ship together so the demo is usable as soon as the job succeeds
- **Credential-driven** — The same OpenShift + AAP credentials pattern used elsewhere in APD; no manual kubeconfig on the controller
- **Safe teardown** — Uninstall is a first-class template so shared demo clusters do not accumulate orphaned AO namespaces

## Presenter walkthrough

1. Confirm an OpenShift cluster is available and the **OpenShift Credential** + **AAP Credential** are attached to the install template
2. Launch **Infrastructure ǀ Automation Orchestrator ǀ Install** — expect several minutes while operators and the Route come up (job timeout is 60 minutes)
3. From the job output, copy the AO URL, `admin` username, and initial password — open the URL in a browser (login may fail for a minute or two after deploy; retry)
4. Optionally re-run **Infrastructure ǀ AO Network Configuration ǀ Install** if you change the AAP gateway hostname or need extra allow-listed hosts
5. When finished, launch **Infrastructure ǀ Automation Orchestrator ǀ Uninstall** to remove AO and related operators/namespaces

## Talking points

- Automation Orchestrator is installed with `aapctl`, the supported CLI path — AAP is driving the same tool an admin would use on the command line
- Network configuration is not optional for AAP integration: AO must trust the gateway hostname (and its own Route) on the integration URL allow-list
- Private-network OIDC is enabled so AAP and AO can authenticate when they share a private OpenShift network
- The AO EE (`quay.io/acme_corp/ao-ee:latest`) packages `aapctl` so Controller does not need cluster-admin tools baked into the default EE

## Related demos

| Demo | Description |
|------|-------------|
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | Provision an OpenShift cluster on AWS to use as the AO deployment target |
| [OPA — Policy as Code](./opa-policy-as-code.md) | Deploy another OpenShift-backed control-plane component from AAP |

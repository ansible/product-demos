# OPA — Policy as Code

Demonstrate AAP's Policy as Code feature using Open Policy Agent (OPA) deployed on OpenShift. The demo deploys an OPA server, loads Rego policies, and configures AAP to evaluate policies before allowing jobs to run.  The OPA server is not configured for production use as it does not require authentication.

## Prerequisites

- OpenShift cluster with privileges to create projects, deployments, services, and routes
- OpenShift Credential configured in AAP (bearer token for cluster authentication)
- AAP Credential configured in AAP (for updating Policy as Code settings)

## Configure credentials

| Credential | Type | Where to get it |
|------------|------|-----------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | OpenShift console — Service Account or user token |
| AAP Credential | Red Hat Ansible Automation Platform | AAP instance — admin credentials |

## Survey prompts

### Deploy Open Policy Agent

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| OPA namespace | `opa_namespace` | text | Yes |
| OPA container image | `opa_image` | text | Yes |

### Add Policy

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| OPA namespace | `opa_namespace` | text | Yes |
| Policy name | `opa_policy_name` | text | Yes |
| Rego policy text | `opa_policy_text` | textarea | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OPA ǀ Deploy Open Policy Agent | [`infrastructure/opa/deploy-opa.yml`](../opa/deploy-opa.yml) | Deploys OPA on OpenShift, loads bundled Rego policies, and configures AAP's Policy as Code settings |
| OPA ǀ Add Policy | [`infrastructure/opa/add-policy.yml`](../opa/add-policy.yml) | Uploads a Rego policy to OPA via the REST API (in-memory only, does not persist across pod restarts) |

## Included policies

### deny_all

A simple policy that denies all job execution. Useful for demonstrating that Policy as Code enforcement is working, or for "maintenance mode" scenarios.

**Query path**: `apd/deny_all`

### common_policies

A combined policy with two checks:

- **Maintenance window** — Restricts job execution to a configurable time window. Supports HH:MM format, wrapping windows (e.g. 22:00–06:00), and timezone configuration.
- **Superuser restriction** — Prevents superuser accounts from running jobs unless explicitly allowed.

**Query path**: `apd/common_policies`

Configure via `policy_as_code_vars` in extra_vars:

```yaml
policy_as_code_vars:
  maintenance_window_start: "06:00"
  maintenance_window_end: "22:00"
  maintenance_window_timezone: "America/New_York"
  allow_superuser: true
```

| Variable | Description | Default |
|----------|-------------|---------|
| `maintenance_window_start` | Start of the allowed execution window (HH:MM, 24-hour) | Not set (no restriction) |
| `maintenance_window_end` | End of the allowed execution window (HH:MM, 24-hour) | Not set (no restriction) |
| `maintenance_window_timezone` | IANA timezone for the maintenance window | `UTC` |
| `allow_superuser` | Allow superuser accounts to run jobs | `false` |

## Why it matters

- **Context-aware enforcement** — Complement AAP RBAC enforcement with additional context - incident freezes, maintenance windows, etc.
- **Flexible scoping** — Apply policies at the organization, inventory, or job template level with per-scope configuration via extra_vars
- **Separation of concerns** — Security and compliance teams can manage Rego policies independently from automation content

## Presenter walkthrough

1. Run **Infrastructure | OPA - Deploy Open Policy Agent on OpenShift** — accept the defaults or customize the namespace and image. After the job completes, confirm the OPA server URL in the output
2. Apply the `apd/deny_all` policy to the demo organization in AAP (Access → Organizations → edit → Policy enforcement → set OPA query path to `apd/deny_all`)
3. Run any job template in that organization — show that it is denied with the message "'Deny all' policy is in effect"
4. Change the organization's policy to `apd/common_policies` — run a job as a regular user to show it is now allowed (no `policy_as_code_vars` configured, so the policy allows all jobs by default)
5. Run the same job as a superuser (e.g. "admin") to demonstrate the superuser restriction
6. Add `policy_as_code_vars` to the organization or job template's extra_vars with a maintenance window that excludes the current time — run the job to show it is denied with a message indicating the allowed window
7. Adjust the maintenance window to include the current time and re-run to show it is allowed
8. Optionally use **Infrastructure | OPA - Add Policy** to upload a custom policy via the REST API, demonstrating runtime policy updates without redeployment

## Talking points

- OPA is a CNCF-graduated project used across the cloud-native ecosystem for policy enforcement
- Rego policies are declarative and testable — they can be version-controlled alongside automation content
- AAP evaluates policies before job execution, not after — violations are caught before any changes are made
- The same OPA server can enforce policies for multiple AAP instances or other systems (Kubernetes admission, API gateways, etc.)
- Maintenance window and superuser restrictions are just examples — any attribute in the AAP job request payload can be used for policy decisions

## Related demos

| Demo | Description |
|------|-------------|
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | Provision an OpenShift cluster on AWS to use as the OPA deployment target |
| [OpenShift CNV](../../openshift/docs/openshift-cnv.md) | Run VMs on an existing OpenShift cluster |

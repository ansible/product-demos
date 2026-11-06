# Automation Orchestrator — Hub (Start Here)

Start here for Automation Orchestrator (AO) on the [Ansible Product Demos catalog item](https://red.ht/apd-sandbox) from [demo.redhat.com](https://demo.redhat.com). OpenShift, credentials, and the AO execution environment are already wired.

Before either path: confirm AO templates exist — if not, run **APD Multi-demo setup** (or **APD Single demo setup** with infrastructure).

## Path 1 — Just install AO

Stupid simple: one job template.

1. Launch **Infrastructure Automation Orchestrator Install**.
2. Open the AO URL from the job output and log in as **admin** with the printed password. Install sets a **48-hour** browser session so demos are less likely to kick you out mid-lab.

You now have AO. On demo.redhat.com, Install also wires the pre-filled Controller **LiteMaaS** credential into AO as an LLM Provider integration so agentic (AI) workflow nodes can run. The Install job template must have **LiteMaaS** attached (APD setup on this branch does that). If the seed summary says LLM was not wired, re-run Install once after setup so the virtual key injects. Seeded demo workflows may still need Path 2 (**Deploy Shared Services**, and Cloud Stack only when you need aws-rhel9 / Multi-OS hosts). Install **warns** on missing deps; it does not fail.

Skip Network Configuration on RHDP — Install already ran it.

## Path 2 — Pre-seeded demos that actually run

Still simple — shared lab services (and cloud VMs only when a demo needs them), then Install.

1. Ensure **APD Multi-demo setup** (or Single demo setup with cloud + infrastructure) created the Cloud AWS patch/snapshot job templates and the OpenFlake / Gitea / Mattermost credential types.
2. Launch **Infrastructure AWS - Deploy Shared Services** ([details](./shared-services.md)). One workflow: VPC + keypair, then Mattermost + Gitea in parallel, plus OpenFlake on OpenShift; when all three succeed it publishes a password-gated S3 credentials portal for this lab. That covers chat (disk-utilization), SCM/Actions (inventory-service + act_runner), and ITSM (OpenFlake) credentials — you do not need separate Provision Mattermost / Provision Gitea / OpenFlake jobs unless you prefer to run them alone. Copy the portal URL and password (`Ansible123!`) from the **Shared Services Portal** nested job.
3. Only if you need disk-utilization or Multi-OS Cloud Patching hosts: also run **Deploy Cloud Stack in AWS** (aws-rhel9, Windows, reports, and so on). Skip for CI/CD Pipeline or Task Step Example alone.
4. Launch **Infrastructure Automation Orchestrator Install**. Soft-failed / retried tasks in the middle are normal on a cold cluster; the job should still finish green (often about 10 minutes). Soft warnings for missing optional deps do not fail Install.
5. Use the **seed summary** at the end of Install for AO URL / admin password (and Mattermost / OpenFlake / Gitea login details when Shared Services ran).
6. For CI/CD: Install creates an AO webhook service account, authorizes it on lightwell-ci-cd, publishes the workflow, and writes Gitea Actions secrets (AO_WEBHOOK_URL + OAuth client). Confirm that in the seed summary, then open the seeded workflow.
7. Open the seeded workflow you want to show.

<aside class="info-callout" role="note">
  <span class="info-callout__icon" aria-hidden="true">i</span>
  <p>Shared Services and Cloud Stack stay opt-in so Path 1 labs are not billed for idle EC2. Prefer Shared Services over hand-running Mattermost, Gitea, and OpenFlake one by one.</p>
</aside>

**You are ready to present.** Curated demos:

| Demo | Directions | Needs |
|------|------------|-------|
| Task Step Example | Open **Task Step Example** in AO — question is pre-filled; press Run | LiteMaaS wired (RHDP boot + Install) |
| Disk utilization | [Disk Utilization & Remediation](https://ansible-tmm.github.io/aap-orchestrator-demos/demos/disk-utilization/) | aws-rhel9 + Mattermost |
| Multi-OS Cloud Patching | [Multi-OS Cloud Patching](https://ansible-tmm.github.io/aap-orchestrator-demos/demos/multi-os-cloud-patching/) | Full cloud stack + existing Cloud AWS patch/snapshot JTs |
| CI/CD Pipeline | [CI/CD Pipeline](https://ansible-tmm.github.io/aap-orchestrator-demos/demos/cicd-pipeline/) | [Gitea](./gitea.md) (inventory-service) + OpenFlake + AO_WEBHOOK_URL. Re-run helper: **CI/CD Demo - Reset Change Request** (default CHG0034907). |

Install rewrites CI/CD close/rollback ServiceNow notes to trigger-based text so an empty AI structured output cannot block the AAP step (no Controller job = expression failed before launch). Seed also forces agentic note nodes to empty tool selections plus `response_schema.required` (LiteMaaS/qwen otherwise often returns `finish_reason: tool_calls` with empty `result.content` while the node still shows completed).

### Task Step Example — LiteMaaS smoke test

No cloud stack. After Install, open **Task Step Example**, leave the default question (or edit it), and Run. Seed injects both the model (`llm_model_id`) and the **APD LiteMaaS** LLM Provider credential (`credential_id`) on the AI task step — model alone is not enough to call LiteMaaS.

### Multi-OS Cloud Patching — manual trigger

The seeded workflow pre-fills inventory limits for the cloud stack. Set **`aws_region`** to the region where you deployed the stack, then run:

```json
{
  "_hosts": "aws-rhel9:aws-rhel10",
  "_hosts_windows": "aws-dc:aws_win1",
  "_report_server": "reports",
  "aws_region": "<your region>"
}
```

## The three AO templates

| Template | When to use it | Playbook |
|----------|----------------|----------|
| **Infrastructure Automation Orchestrator Install** | Path 1 — stands up AO, wires AAP, seeds demos from [demos.yml](../ao/demos.yml). | [install.yml](../ao/install.yml) |
| **Infrastructure AO Network Configuration Install** | Rare re-run of allow-listing. **Skip on RHDP.** | [network-access.yml](../ao/network-access.yml) |
| **Infrastructure Automation Orchestrator Uninstall** | Tear down AO when the lab session is done. Waits until the automation-orchestrator namespace is gone so Install can be re-run cleanly. | [uninstall.yml](../ao/uninstall.yml) |

## Configure credentials

| Credential | Type | On demo.redhat.com |
|------------|------|--------------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | Pre-configured |
| AAP Credential | Red Hat Ansible Automation Platform | Pre-configured |
| LiteMaaS | Custom (API base URL + virtual key + model) | Pre-configured at catalog boot; Install wires it into AO |
| Mattermost | Custom (server + webhook id) | Path 2 — Deploy Shared Services (or Provision Mattermost alone) |
| OpenFlake | Custom (instance URL + admin) | Path 2 — Deploy Shared Services (or OpenFlake alone) |
| Gitea | Custom (host/port/token/owner/repo) | Path 2 — Deploy Shared Services (or Provision Gitea alone) |

## Under the hood

What **Install** does when it seeds curated demos:

- Reads [`demos.yml`](../ao/demos.yml) and seeds entries with `enabled: true` from [aap-orchestrator-demos](https://github.com/ansible-tmm/aap-orchestrator-demos) (**disk-utilization**, **multi-os-cloud-patching**, **cicd-pipeline**) plus local workflows such as **Task Step Example**.
- Creates the **AAP Orchestrator Demos** project and any demo-owned job templates (disk-utilization / CI/CD playbooks). Multi-OS reuses existing **Cloud | AWS |*** templates from cloud setup — seed only imports the workflow.
- Wires AO-native **AAP** and **LiteMaaS** (LLM Provider) integrations; allow-lists the LiteMaaS hostname for AO workers.
- Rewrites each workflow’s AAP org/credential placeholders → APD, and fills `llm_model_id` on agentic nodes when LiteMaaS is wired, then imports into AO.
- When present, attaches the **Mattermost** credential and **Product Demos EE** to **Notify Chatroom**.
- When present, attaches **OpenFlake** and **Gitea** credentials to the CI/CD Pipeline job templates; soft-warns when they are still stubs.

AAP drives this with `aapctl`. The Mattermost credential stores an **incoming webhook** id for `community.general.mattermost` (not a bot personal access token). Controller **LiteMaaS** is the source of truth for the virtual key; AO gets a copy as **APD LiteMaaS** during Install. APD does **not** run upstream `cicd_setup_gitea` (that would wipe the shared Gitea host); Provision Gitea owns the forge bootstrap.

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Deploy Shared Services](./shared-services.md) | Path 2 default — VPC + keypair + Mattermost + Gitea + OpenFlake |
| [AWS Mattermost](./mattermost.md) | Standalone chat backend (prefer Shared Services) |
| [AWS Gitea](./gitea.md) | Standalone SCM + Actions runner (prefer Shared Services) |
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | OpenShift on AWS when you are not using RHDP |
| [OPA — Policy as Code](./opa-policy-as-code.md) | Another OpenShift-backed control-plane component from AAP |

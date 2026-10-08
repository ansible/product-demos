# Automation Orchestrator — Hub (Start Here)

Start here for Automation Orchestrator (AO) on the [Ansible Product Demos catalog item](https://red.ht/apd-sandbox) from [demo.redhat.com](https://demo.redhat.com). OpenShift, credentials, and the AO execution environment are already wired.

Before either path: confirm AO templates exist — if not, run **APD ǀ Multi-demo setup** (or **APD ǀ Single demo setup** → `infrastructure`).

## Path 1 — Just install AO

Stupid simple: one job template.

1. Launch **Infrastructure ǀ Automation Orchestrator ǀ Install**.
2. Open the AO URL from the job output and log in as `admin` with the printed password.

You now have AO. Seeded demo workflows may appear in AO, but they will not run end-to-end without Path 2 (no `aws_rhel9`, no Mattermost, and so on). Install **warns** on missing deps; it does not fail.

Skip Network Configuration on RHDP — Install already ran it.

## Path 2 — Pre-seeded demos that actually run

Still simple — short cloud/chat setup, then Install, so curated content can hit real hosts (and chat when the demo needs it).

1. Ensure **APD ǀ Multi-demo setup** (or Single → `cloud` + `infrastructure`) created the **Cloud | AWS |*** patch/snapshot JTs.
2. Run **Deploy Cloud Stack in AWS** (full stack for Multi-OS; disk-utilization only needs `aws_rhel9`).
3. For demos that post to chat (disk-utilization): launch **Infrastructure ǀ AWS - Provision Mattermost** ([details](./mattermost.md)). Skip for Multi-OS Cloud Patching.
4. Launch **Infrastructure ǀ Automation Orchestrator ǀ Install**.
5. Use the **seed summary** at the end of Install for AO URL / admin password (and Mattermost URL + login when provisioned).
6. Open the seeded workflow you want to show.

<aside class="info-callout" role="note">
  <span class="info-callout__icon" aria-hidden="true">i</span>
  <p>Cloud Stack and Mattermost stay opt-in so shared labs are not billed for idle EC2 when you only wanted Path 1.</p>
</aside>

**You are ready to present.** Curated demos:

| Demo | Directions | Needs |
|------|------------|-------|
| Disk utilization | [Disk Utilization & Remediation](https://ansible-tmm.github.io/aap-orchestrator-demos/demos/disk-utilization/) | `aws_rhel9` + Mattermost |
| Multi-OS Cloud Patching | [Multi-OS Cloud Patching](https://ansible-tmm.github.io/aap-orchestrator-demos/demos/multi-os-cloud-patching/) | Full cloud stack + existing **Cloud \| AWS \|*** JTs |

## The three AO templates

| Template | When to use it | Playbook |
|----------|----------------|----------|
| **Infrastructure ǀ Automation Orchestrator ǀ Install** | Path 1 — stands up AO, wires AAP, seeds demos from [`demos.yml`](../ao/demos.yml). | [`install.yml`](../ao/install.yml) |
| **Infrastructure ǀ AO Network Configuration ǀ Install** | Rare re-run of allow-listing. **Skip on RHDP.** | [`network-access.yml`](../ao/network-access.yml) |
| **Infrastructure ǀ Automation Orchestrator ǀ Uninstall** | Tear down AO when the lab session is done. Waits until the `automation-orchestrator` namespace is gone so Install can be re-run cleanly. | [`uninstall.yml`](../ao/uninstall.yml) |

## Configure credentials

| Credential | Type | On demo.redhat.com |
|------------|------|--------------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | Pre-configured |
| AAP Credential | Red Hat Ansible Automation Platform | Pre-configured |
| Mattermost | Custom (server + webhook id) | Path 2 — created/updated by **Provision Mattermost** |

## Under the hood

What **Install** does when it seeds curated demos:

- Reads [`demos.yml`](../ao/demos.yml) and seeds entries with `enabled: true` from [aap-orchestrator-demos](https://github.com/ansible-tmm/aap-orchestrator-demos) (**disk-utilization**, **multi-os-cloud-patching**).
- Creates the **AAP Orchestrator Demos** project and any demo-owned job templates (disk-utilization playbooks). Multi-OS reuses existing **Cloud | AWS |*** templates from cloud setup — seed only imports the workflow.
- Rewrites each workflow’s AAP org/credential placeholders → APD, then imports it into AO.
- When present, attaches the **Mattermost** credential and **Product Demos EE** to **Notify Chatroom**.

AAP drives this with `aapctl`. The Mattermost credential stores an **incoming webhook** id for `community.general.mattermost` (not a bot personal access token).

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Mattermost](./mattermost.md) | Path 2 — chat backend + Controller credential |
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | OpenShift on AWS when you are not using RHDP |
| [OPA — Policy as Code](./opa-policy-as-code.md) | Another OpenShift-backed control-plane component from AAP |

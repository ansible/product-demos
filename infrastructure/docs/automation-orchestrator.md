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

Still simple — same Install as Path 1 — plus a short setup so curated content can hit a real host and post to chat. **Before** Path 1, run:

| Run | Piece | Why |
|-----|-------|-----|
| **Deploy Cloud Stack in AWS**, then sync **AWS Inventory** | `aws_rhel9` in inventory | Disk check / remediate target |
| **Infrastructure ǀ AWS - Provision Mattermost** ([details](./mattermost.md)), then sync inventory | Mattermost + Controller credential | Notify Chatroom posts |
| Matching APD template when a seeded demo catalogs it | AI endpoints or other backends | Only for demos that need them |

<aside class="info-callout" role="note">
  <span class="info-callout__icon" aria-hidden="true">i</span>
  <p>Cloud Stack and Mattermost stay opt-in so shared labs are not billed for idle EC2 when you only wanted Path 1.</p>
</aside>

Then complete **Path 1** (Install + login) and open the seeded workflow you want to show.

**You are ready to present.** Curated demos:

| Demo | Directions |
|------|------------|
| Disk utilization | [Disk Utilization & Remediation](https://ansible-tmm.github.io/aap-orchestrator-demos/demos/disk-utilization/) |

## The three AO templates

| Template | When to use it | Playbook |
|----------|----------------|----------|
| **Infrastructure ǀ Automation Orchestrator ǀ Install** | Path 1 — stands up AO, wires AAP, seeds demos from [`demos.yml`](../ao/demos.yml). | [`install.yml`](../ao/install.yml) |
| **Infrastructure ǀ AO Network Configuration ǀ Install** | Rare re-run of allow-listing. **Skip on RHDP.** | [`network-access.yml`](../ao/network-access.yml) |
| **Infrastructure ǀ Automation Orchestrator ǀ Uninstall** | Tear down AO when the lab session is done. | [`uninstall.yml`](../ao/uninstall.yml) |

## Configure credentials

| Credential | Type | On demo.redhat.com |
|------------|------|--------------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | Pre-configured |
| AAP Credential | Red Hat Ansible Automation Platform | Pre-configured |
| Mattermost | Custom (server + webhook id) | Path 2 — created/updated by **Provision Mattermost** |

## Under the hood

What **Install** does when it seeds curated demos:

- Reads [`demos.yml`](../ao/demos.yml) and seeds entries with `enabled: true` (today: **disk-utilization** from [aap-orchestrator-demos](https://github.com/ansible-tmm/aap-orchestrator-demos)).
- Creates the **AAP Orchestrator Demos** project and those demo job templates in org **Ansible Product Demos (APD)**.
- Rewrites each workflow’s `organization_name` from `Default` → APD, then imports it into AO.
- When present, attaches the **Mattermost** credential and **Product Demos EE** to **Notify Chatroom**.

AAP drives this with `aapctl`. The Mattermost credential stores an **incoming webhook** id for `community.general.mattermost` (not a bot personal access token).

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Mattermost](./mattermost.md) | Path 2 — chat backend + Controller credential |
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | OpenShift on AWS when you are not using RHDP |
| [OPA — Policy as Code](./opa-policy-as-code.md) | Another OpenShift-backed control-plane component from AAP |

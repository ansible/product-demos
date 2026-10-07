# Automation Orchestrator — Hub (Start Here)

Start here for Automation Orchestrator (AO) on the [Ansible Product Demos catalog item](https://red.ht/apd-sandbox) from [demo.redhat.com](https://demo.redhat.com). OpenShift, credentials, and the AO execution environment are already wired.

## Presenter walkthrough

Do these in order. When you finish step 5, you have **AO + the disk-utilization demo ready to present**.

1. Confirm AO templates exist — if not, run **APD ǀ Multi-demo setup** (or **APD ǀ Single demo setup** → `infrastructure`).
2. **Deploy Cloud Stack in AWS** → wait until `aws_rhel9` is in inventory (sync **AWS Inventory** if needed).
3. **Infrastructure ǀ AWS - Provision Mattermost** → confirm Controller credential **Mattermost** was updated ([details](./mattermost.md)).
4. Sync **AWS Inventory** again.
5. **Infrastructure ǀ Automation Orchestrator ǀ Install** → from the job output, open the AO URL, log in as `admin` with the printed password, and open the seeded **disk-utilization** workflow.

**You are ready to present** — run the workflow in AO (disk check → remediate → Mattermost notify on channel `apd-notify`).

6. When the session is over → **Infrastructure ǀ Automation Orchestrator ǀ Uninstall**.

Skip Network Configuration on RHDP — Install already ran it.

Only need AO itself (no disk demo / no chat)? Run steps **1** and **5**, then **6** when done. Install **warns** if `aws_rhel9` or Mattermost is missing; it does not fail.

## The three AO templates

| Template | When to use it | Playbook |
|----------|----------------|----------|
| **Infrastructure ǀ Automation Orchestrator ǀ Install** | Step 5 — stands up AO, wires AAP, seeds demos from [`demos.yml`](../ao/demos.yml). | [`install.yml`](../ao/install.yml) |
| **Infrastructure ǀ AO Network Configuration ǀ Install** | Rare re-run of allow-listing. **Skip on RHDP.** | [`network-access.yml`](../ao/network-access.yml) |
| **Infrastructure ǀ Automation Orchestrator ǀ Uninstall** | Step 6 — tear down when finished. | [`uninstall.yml`](../ao/uninstall.yml) |

## Why don't we just provision everything?

Cloud Stack and Mattermost are **not** part of AO Install on purpose:

- **Cost** — Shared RHDP labs already burn OpenShift + AAP. Auto-creating EC2 on every Install leaves idle hosts and drives AWS spend.
- **Choice** — Presenters who only want the AO UI skip steps 2–4.
- **Soft preflight** — Missing deps warn at Install time; AO still comes up.

## Configure credentials

| Credential | Type | On demo.redhat.com |
|------------|------|--------------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | Pre-configured |
| AAP Credential | Red Hat Ansible Automation Platform | Pre-configured |
| Mattermost | Custom (server + webhook id) | Created/updated by **Provision Mattermost** (step 3) |

## Under the hood

Install seeds demos with `enabled: true` in [`demos.yml`](../ao/demos.yml) (today: **disk-utilization** from [aap-orchestrator-demos](https://github.com/ansible-tmm/aap-orchestrator-demos)). It creates project **AAP Orchestrator Demos** and demo JTs in org **Ansible Product Demos (APD)**, rewrites workflow `organization_name` from `Default` → APD, attaches **Mattermost** + **Product Demos EE** to **Notify Chatroom** when present, and imports the workflow into AO. AAP drives `aapctl`; the Mattermost credential holds an **incoming webhook** id for `community.general.mattermost`.

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Mattermost](./mattermost.md) | Step 3 — chat backend + Controller credential |
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | OpenShift on AWS when you are not using RHDP |
| [OPA — Policy as Code](./opa-policy-as-code.md) | Another OpenShift-backed control-plane component from AAP |

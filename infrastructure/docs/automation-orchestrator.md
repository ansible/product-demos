# Automation Orchestrator — Hub (Start Here)

Start here for Automation Orchestrator (AO) on the [Ansible Product Demos catalog item](https://red.ht/apd-sandbox) from [demo.redhat.com](https://demo.redhat.com). OpenShift, credentials, and the AO execution environment are already wired — you do not assemble a platform from scratch.

This page is the **hub**. The three AO job templates are listed below. Optional AWS pieces (cloud stack, Mattermost) are **not** installed by AO Install on purpose — see [Why don't we just provision everything?](#why-dont-we-just-provision-everything).

## The three AO templates

| Template | When to use it | Playbook |
|----------|----------------|----------|
| **Infrastructure ǀ Automation Orchestrator ǀ Install** | Main path. Runs `aapctl`, network allow-list, AAP integration, and seeds curated demos from [`demos.yml`](../ao/demos.yml). | [`install.yml`](../ao/install.yml) |
| **Infrastructure ǀ AO Network Configuration ǀ Install** | Optional re-run of allow-listing / private-network OIDC. **Skip on RHDP** — Install already did this. | [`network-access.yml`](../ao/network-access.yml) |
| **Infrastructure ǀ Automation Orchestrator ǀ Uninstall** | Tear down AO when the demo is done so the shared cluster stays clean. | [`uninstall.yml`](../ao/uninstall.yml) |

## Prerequisites

- **If using RHDP (demo.redhat.com):** OpenShift, **OpenShift Credential**, **AAP Credential**, and **AO Execution Environment** ship with the catalog item. Run **APD ǀ Multi-demo setup** (or **APD ǀ Single demo setup** → `infrastructure`) if the AO templates are not visible yet.
- **If using your own installation:** OpenShift cluster, OpenShift + AAP credentials, AO EE (`quay.io/acme_corp/ao-ee:latest`), and **APD ǀ Single demo setup** with category `infrastructure`.

Install alone is enough to get AO up and log in. Extra jobs below are only needed if you want the **seeded demo workflows** (for example disk utilization) to run end-to-end against real hosts and chat.

## Optional — make seeded AO demos work

Install seeds workflows and job templates from [`infrastructure/ao/demos.yml`](../ao/demos.yml) (today: **disk-utilization** from [aap-orchestrator-demos](https://github.com/ansible-tmm/aap-orchestrator-demos)). Those templates call existing APD inventory and credentials. They are **not required** to open AO — only to run the demo story.

| Goal | Run this | Why |
|------|----------|-----|
| Disk check / remediate against a RHEL host | **Deploy Cloud Stack in AWS**, then sync **AWS Inventory** so `aws_rhel9` exists | Seeded JTs limit to `aws_rhel9`. Install **warns** if it is missing but still seeds. |
| Notify Chatroom posts to Mattermost | **Infrastructure ǀ AWS - Provision Mattermost** (writes the **Mattermost** Controller credential), sync inventory, re-run **AO Install** so Notify Chatroom attaches that credential and **Product Demos EE** | `community.general.mattermost` needs `mattermost_server` + incoming webhook id (`api_chat_token`). See [Mattermost](./mattermost.md). |
| Expand EBS during disk-expand remediation | Cloud stack host + **AWS** credential on the expand JT (Install attaches AWS when the catalog says so) | Same cloud stack as above. |

Suggested order when you want the full disk demo:

1. **Deploy Cloud Stack in AWS** → wait for `aws_rhel9`
2. **Infrastructure ǀ AWS - Provision Mattermost** → confirm credential **Mattermost** was updated
3. Sync **AWS Inventory**
4. **Infrastructure ǀ Automation Orchestrator ǀ Install**
5. Open the AO URL from the job output (`admin` + printed password) → run the seeded disk-utilization workflow
6. When finished → **Uninstall**

## Why don't we just provision everything?

AO Install turns on Automation Orchestrator and seeds workflow definitions. It does **not** also launch Cloud Stack, Mattermost, Kafka, or every other lab VM.

- **Cost** — Shared RHDP labs already burn OpenShift + AAP. Auto-creating EC2 for every AO install (even when the presenter only wants the AO UI) would leave idle hosts running and drive up AWS spend.
- **Choice** — Many presenters only need AO itself. Optional deps stay opt-in: run them when the seeded JT path needs them; skip them when you do not.
- **Soft preflight** — Missing `aws_rhel9` or Mattermost produces a **warning** at Install time, not a hard failure, so AO still comes up.

If a dependency is missing later, run the matching APD template and re-run Install (or attach the Mattermost credential manually) — you do not need to rebuild AO from scratch.

## Configure credentials

| Credential | Type | On demo.redhat.com |
|------------|------|--------------------|
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | Pre-configured |
| AAP Credential | Red Hat Ansible Automation Platform | Pre-configured |
| Mattermost | Custom (server + webhook id) | Created/updated by **Provision Mattermost** |

## What Install seeds

Install only seeds demos with `enabled: true` in [`infrastructure/ao/demos.yml`](../ao/demos.yml).

On seed, Install:

1. Creates AAP project **AAP Orchestrator Demos** and the demo job templates in org **Ansible Product Demos (APD)** — not declared permanently in `setup.yml`
2. Rewrites workflow JSON `organization_name` from `Default` → **Ansible Product Demos (APD)** and injects AO AAP credential/integration IDs
3. Attaches **Mattermost** credential + **Product Demos EE** to **Notify Chatroom** when present
4. Imports the selected workflow into AO (idempotent create/update by `source_file` label)

To add another demo later: append a catalog entry and set `enabled: true`.

## Why it matters

- **Demo-ready on RHDP** — Cluster and credentials are already there; the story is “press Launch,” not “assemble a platform”
- **AO boots with a real workflow** — disk utilization check → switch → remediate → notify, not an empty canvas
- **No JT sprawl** — demo job templates appear at Install time from the catalog
- **Clean exit** — Uninstall is first-class so shared labs do not keep orphaned AO namespaces
- **Pay for what you use** — cloud/chat backends stay optional

## Talking points

- Supported path: AAP drives `aapctl`, the same CLI an admin would use
- Seeding reuses normalize/import (aap-demo style), filtered by a YAML allowlist
- Upstream exports say `organization_name: Default`; APD rewrites that to the APD org at import time
- Mattermost credential holds an **incoming webhook** id for `community.general.mattermost`, not only a bot PAT

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Mattermost](./mattermost.md) | Optional chat backend + Controller credential for Notify Chatroom |
| [ROSA Cluster Lifecycle](./rosa-lifecycle.md) | OpenShift on AWS when you are not using the RHDP catalog item |
| [OPA — Policy as Code](./opa-policy-as-code.md) | Another OpenShift-backed control-plane component launched from AAP |

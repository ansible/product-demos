# AWS Gitea

Stand up a lightweight self-hosted Git forge on AWS for demos that need SCM without GitHub.com — including the AO **CI/CD Pipeline** demo (`inventory-service` + Gitea Actions).

## Prerequisites

- Shared AWS networking in the target region (defaults: `aws-test-subnet`, `aws-test-sg`, `aws-test-key`). Prefer:
  - **[Infrastructure ǀ AWS - Deploy Shared Services](./shared-services.md)** (one-click VPC + keypair + Mattermost + Gitea), or
  - **Cloud ǀ AWS ǀ Create VPC** + **Cloud ǀ AWS ǀ Create Keypair**, or
  - reuse an existing **Deploy Cloud Stack in AWS** (full stack is fine, but not required — Gitea does not need the five demo VMs)
- **AWS**, **APD Machine Credential**, and **AAP Credential** configured (AAP Credential is required so Provision Gitea can upsert the **Gitea** credential on Controller)

## Configure credentials

| Credential | Type | Notes |
|------------|------|-------|
| AWS | Amazon Web Services | EC2 create + security group |
| APD Machine Credential | Machine | SSH as `ec2-user` to configure Podman |
| AAP Credential | Red Hat Ansible Automation Platform | Controller API for **Gitea** credential write-back |

## Survey prompts

| Prompt | Variable | Default |
|--------|----------|---------|
| AWS Region | `create_vm_aws_region` | `us-east-2` |
| Owner | `create_vm_aws_owner_tag` | `your_name` (must match the owner tag on VPC/keypair resources) |
| Environment | `create_vm_vm_environment` | `Prod` |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Infrastructure ǀ AWS - Provision Gitea | [`infrastructure/gitea/provision_gitea.yml`](../gitea/provision_gitea.yml) | EC2 `aws_gitea` + Podman Gitea (SQLite) + admin + CI/CD bootstrap |

## Why it matters

- One reusable Git forge for demos that need to push/pull without GitHub.com
- Same cloud networking pattern as **Provision Mattermost** / **Provision Kafka Queue**
- Seeds `apdadmin/inventory-service` at the Lightwell vulnerable baseline (`aiohttp==3.9.0`, empty `PATCHED_CVE` / `CHANGE_REQUEST`, `app.py` + tests + Actions CI), enables Actions, starts `act_runner`, installs inventory-service **dev (:8080) / prod (:80)** runtimes on the same host, and upserts the **Gitea** credential for AO Install
- **Simulate Lightwell PR** patches to `aiohttp==3.9.0.rhlw-00001` (same 3.9.0, backport suffix only); **Reset Demo** restores `aiohttp==3.9.0` for repeatable runs
- Re-run apps only via **Infrastructure ǀ AWS - Setup CI/CD Demo Host** (limit `aws_gitea`) without reprovisioning Gitea
- Job output prints the URL and default login so students can open Gitea immediately

## Presenter walkthrough

1. Prefer **Infrastructure ǀ AWS - Deploy Shared Services** for one-click networking + Gitea (and Mattermost). Or ensure networking exists via **Create VPC** + **Create Keypair** / cloud stack, then launch **Infrastructure ǀ AWS - Provision Gitea** alone
2. At the end of the job, copy the printed **URL / Username / Password** block — also note `apdadmin/inventory-service`
3. Open the URL in a browser and sign in — default login is `apdadmin` / `Ansible123!`
4. Run **AO Install** (with the **Gitea** credential attached) — seed writes Actions secret **`AO_WEBHOOK_URL`** for `lightwell-ci-cd` automatically

Default admin login is `apdadmin` / `Ansible123!` (same as Mattermost; username `admin` is reserved by Gitea). Change it for long-lived labs.

## Talking points

- Gitea runs as a Podman container with SQLite on a dedicated RHEL 9 EC2 host; Actions enabled
- Companion `gitea-runner` (`act_runner`) uses the host Podman socket
- Ports **3000**, **80**, and **8080** are opened on `aws-test-sg` (Gitea UI + demo app ports used by CI/CD Setup Demo Host)
- Connection details are also written to `/etc/apd-gitea.env` on the host
- Sync **AWS Inventory** afterward if you need `aws_gitea` as a managed host in Controller
- APD does **not** run upstream `cicd_setup_gitea` — that would wipe this shared host; Provision Gitea owns the forge bootstrap

## Related demos

| Demo | Description |
|------|-------------|
| [Automation Orchestrator](./automation-orchestrator.md) | Path 2 — CI/CD Pipeline seed attaches the **Gitea** credential |
| [AWS Deploy Shared Services](./shared-services.md) | Preferred one-click path (VPC + keypair + Mattermost + Gitea) |
| [AWS — Create VPC](../../cloud/docs/cloud-create-vpc.md) | Minimal networking prerequisite (no full cloud stack) |
| [AWS — Create Keypair](../../cloud/docs/cloud-create-keypair.md) | SSH key used by APD Machine Credential |
| [AWS Mattermost](./mattermost.md) | Sibling AWS service host pattern (`aws_mattermost`) |
| [Config Drift — Kafka Queue](./config-drift-kafka.md) | Sibling AWS service host pattern (`aws_kafka`) |

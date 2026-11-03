# AWS Gitea

Stand up a lightweight self-hosted Git server on AWS for demos that need a simple SCM endpoint (AI-generated playbooks, student labs, or any workflow that pushes to Git without depending on GitHub.com).

## Prerequisites

- Shared AWS networking in the target region (defaults: `aws-test-subnet`, `aws-test-sg`, `aws-test-key`). Prefer:
  - **[Infrastructure ǀ AWS - Deploy Shared Services](./shared-services.md)** (one-click VPC + keypair + Mattermost + Gitea), or
  - **Cloud ǀ AWS ǀ Create VPC** + **Cloud ǀ AWS ǀ Create Keypair**, or
  - reuse an existing **Deploy Cloud Stack in AWS** (full stack is fine, but not required — Gitea does not need the five demo VMs)
- **AWS** and **APD Machine Credential** configured

## Configure credentials

| Credential | Type | Notes |
|------------|------|-------|
| AWS | Amazon Web Services | EC2 create + security group |
| APD Machine Credential | Machine | SSH as `ec2-user` to configure Podman |

## Survey prompts

| Prompt | Variable | Default |
|--------|----------|---------|
| AWS Region | `create_vm_aws_region` | `us-east-2` |
| Owner | `create_vm_aws_owner_tag` | `your_name` (must match the owner tag on VPC/keypair resources) |
| Environment | `create_vm_vm_environment` | `Prod` |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Infrastructure ǀ AWS - Provision Gitea | [`infrastructure/gitea/provision_gitea.yml`](../gitea/provision_gitea.yml) | EC2 `aws_gitea` + Podman Gitea (SQLite) + admin user |

## Why it matters

- One reusable Git forge for demos that need to push/pull playbooks without GitHub.com
- Same cloud networking pattern as **Provision Mattermost** / **Provision Kafka Queue**
- Job output prints the URL and default login so students can open Gitea immediately

## Presenter walkthrough

1. Prefer **Infrastructure ǀ AWS - Deploy Shared Services** for one-click networking + Gitea (and Mattermost). Or ensure networking exists via **Create VPC** + **Create Keypair** / cloud stack, then launch **Infrastructure ǀ AWS - Provision Gitea** alone
2. At the end of the job, copy the printed **URL / Username / Password** block
3. Open the URL in a browser and sign in — default login is `admin` / `Ansible123!`

Default admin login is `admin` / `Ansible123!` (same password pattern as Mattermost). Change it for long-lived labs.

## Talking points

- Gitea runs as a single Podman container with SQLite on a dedicated RHEL 9 EC2 host
- Port **3000** is opened on `aws-test-sg` and firewalld
- Connection details are also written to `/etc/apd-gitea.env` on the host
- Sync **AWS Inventory** afterward if you need `aws_gitea` as a managed host in Controller

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Deploy Shared Services](./shared-services.md) | Preferred one-click path (VPC + keypair + Mattermost + Gitea) |
| [AWS — Create VPC](../../cloud/docs/cloud-create-vpc.md) | Minimal networking prerequisite (no full cloud stack) |
| [AWS — Create Keypair](../../cloud/docs/cloud-create-keypair.md) | SSH key used by APD Machine Credential |
| [AWS Mattermost](./mattermost.md) | Sibling AWS service host pattern (`aws_mattermost`) |
| [Config Drift — Kafka Queue](./config-drift-kafka.md) | Sibling AWS service host pattern (`aws_kafka`) |

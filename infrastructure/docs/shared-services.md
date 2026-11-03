# AWS Deploy Shared Services

One-click workflow that stands up shared AWS networking plus Mattermost and Gitea — without provisioning the five **Deploy Cloud Stack** demo VMs.

## Prerequisites

- **AWS**, **APD Machine Credential**, and **AAP Credential** configured
- Cloud job templates already present from common/APD setup (**Create VPC**, **Create Keypair**)
- Infrastructure demo setup run so **Provision Mattermost** and **Provision Gitea** exist

## Configure credentials

| Credential | Type | Notes |
|------------|------|-------|
| AWS | Amazon Web Services | VPC, keypair, EC2 for Mattermost/Gitea |
| APD Machine Credential | Machine | SSH as `ec2-user`; Create Keypair derives the public key from this credential |
| AAP Credential | Red Hat Ansible Automation Platform | Required by **Provision Mattermost** to upsert the Mattermost Controller credential |

## Survey prompts

| Prompt | Variable | Default |
|--------|----------|---------|
| AWS Region | `create_vm_aws_region` | `us-east-2` |
| Owner | `create_vm_aws_owner_tag` | `your_name` |
| Environment | `create_vm_vm_environment` | `Prod` |

## Job templates

| Template | Playbook / workflow | Description |
|----------|---------------------|-------------|
| Infrastructure ǀ AWS - Deploy Shared Services | Workflow in [`infrastructure/setup.yml`](../setup.yml) | Create VPC + keypair, then Mattermost and Gitea in parallel |
| Infrastructure ǀ AWS - Provision Mattermost | [`infrastructure/mattermost/provision_mattermost.yml`](../mattermost/provision_mattermost.yml) | Leaf JT (also runnable alone) |
| Infrastructure ǀ AWS - Provision Gitea | [`infrastructure/gitea/provision_gitea.yml`](../gitea/provision_gitea.yml) | Leaf JT (also runnable alone) |

## Why it matters

- Shared chat + Git for labs without waiting on a full cloud stack
- Same `aws-test-*` networking defaults as Mattermost/Gitea standalone jobs
- Prefer this over manual Create VPC → Create Keypair → two provision jobs

## Presenter walkthrough

1. Launch **Infrastructure ǀ AWS - Deploy Shared Services** (region + owner + environment)
2. Wait for Create VPC and Create Keypair to finish, then Mattermost and Gitea in parallel
3. From the Mattermost job output, save the UI login (`apdadmin` / `Ansible123!`) and confirm the Controller credential was updated
4. From the Gitea job output, save the URL and login (`apdadmin` / `Ansible123!`)
5. Optional: run AO Install if you need Notify Chatroom wired to Mattermost

## Talking points

- Does **not** create `aws-rhel9`, Windows, or reports hosts — use **Deploy Cloud Stack in AWS** when you need those
- Mattermost opens TCP **8065**; Gitea opens TCP **3000** (UI) plus **80**/**8080** (CI/CD demo app) on `aws-test-sg`
- Provision Gitea also seeds `inventory-service`, starts an Actions runner, and upserts the **Gitea** credential for AO CI/CD Pipeline
- Kafka and other shared hosts can be added as parallel nodes later

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Mattermost](./mattermost.md) | Standalone Mattermost provision |
| [AWS Gitea](./gitea.md) | Standalone Gitea provision |
| [Deploy Cloud Stack in AWS](../../cloud/docs/deploy-cloud-stack.md) | Full stack including demo VMs |

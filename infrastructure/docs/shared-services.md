# AWS Deploy Shared Services

One-click workflow that stands up shared lab services — AWS networking plus Mattermost and Gitea, and OpenFlake on OpenShift — without provisioning the five **Deploy Cloud Stack** demo VMs. When Mattermost, Gitea, and OpenFlake all succeed, the workflow publishes a password-gated S3 credentials portal for this lab.

## Prerequisites

- **AWS**, **APD Machine Credential**, **AAP Credential**, and **OpenShift Credential** configured
- Cloud job templates already present from common/APD setup (**Create VPC**, **Create Keypair**)
- Infrastructure demo setup run so **Provision Mattermost**, **Provision Gitea**, **OpenFlake**, and **Shared Services Portal** exist

## Configure credentials

| Credential | Type | Notes |
|------------|------|-------|
| AWS | Amazon Web Services | VPC, keypair, EC2 for Mattermost/Gitea; S3 portal bucket |
| APD Machine Credential | Machine | SSH as `ec2-user`; Create Keypair derives the public key from this credential |
| AAP Credential | Red Hat Ansible Automation Platform | Required by provision jobs to upsert Mattermost / Gitea / OpenFlake Controller credentials |
| OpenShift Credential | OpenShift or Kubernetes API Bearer Token | Required by **Infrastructure \| OpenFlake** (OpenShift Helm install) |
| Mattermost / Gitea / OpenFlake | Custom (stubs filled by provision jobs) | Attached to **Shared Services Portal** so injectors supply live URLs/passwords |

## Survey prompts

| Prompt | Variable | Default |
|--------|----------|---------|
| AWS Region | `create_vm_aws_region` | `us-east-2` (dropdown of APD-enabled regions) |

Owner and environment are fixed in workflow extra vars (`apd` / `Prod`) so labs stay one-size-fits-all. OpenFlake runs with `openflake_operation: install` from the same extra vars (no survey question).

## Job templates

| Template | Playbook / workflow | Description |
|----------|---------------------|-------------|
| Infrastructure ǀ AWS - Deploy Shared Services | Workflow in [`infrastructure/setup.yml`](../setup.yml) | Create VPC + keypair → Mattermost + Gitea in parallel; OpenFlake from the start; credentials portal after all three succeed |
| Infrastructure ǀ AWS - Provision Mattermost | [`infrastructure/mattermost/provision_mattermost.yml`](../mattermost/provision_mattermost.yml) | Leaf JT (also runnable alone) |
| Infrastructure ǀ AWS - Provision Gitea | [`infrastructure/gitea/provision_gitea.yml`](../gitea/provision_gitea.yml) | Leaf JT (also runnable alone) |
| Infrastructure ǀ OpenFlake | [`infrastructure/openflake/provision.yml`](../openflake/provision.yml) | Leaf JT (also runnable alone) |
| Infrastructure ǀ AWS - Shared Services Portal | [`infrastructure/shared-services/publish_credentials_portal.yml`](../shared-services/publish_credentials_portal.yml) | Leaf JT — S3 password-gated page for this lab’s logins |

## Why it matters

- Shared chat + Git + ITSM for labs without waiting on a full cloud stack
- Same `aws-test-*` networking defaults as Mattermost/Gitea standalone jobs
- OpenFlake credential write-back enables AO **CI/CD Pipeline** without a real ServiceNow
- One portal URL + password instead of digging through three nested job outputs
- Prefer this over manual Create VPC → Create Keypair → three provision jobs

## Presenter walkthrough

1. Launch **Infrastructure AWS - Deploy Shared Services** (pick region only)
2. OpenFlake starts immediately on OpenShift; Create VPC and Create Keypair run in parallel, then Mattermost and Gitea
3. After all three succeed, **Shared Services Portal** publishes an S3 site. Open that nested job and copy the **Portal URL** and **Portal password** (`Ansible123!`) from the last task
4. Open the portal URL, enter the portal password, and use the unlocked Mattermost / Gitea / OpenFlake cards (copy buttons for URL, user, password)
5. Optional: confirm each Controller credential was upserted (Mattermost, Gitea, OpenFlake) if you care about AO wiring details
6. Optional: run AO Install if you need Notify Chatroom + CI/CD Pipeline seeded

## Talking points

- Does **not** create `aws-rhel9`, Windows, or reports hosts — use **Deploy Cloud Stack in AWS** when you need those
- Mattermost opens TCP **8065**; Gitea opens TCP **3000** (UI) plus **80**/**8080** (CI/CD demo app) on `aws-test-sg`
- Provision Gitea also seeds `inventory-service`, starts an Actions runner, installs inventory-service dev/prod runtimes on `aws_gitea`, and upserts the **Gitea** credential for AO CI/CD Pipeline
- OpenFlake does not use the AWS VPC — it installs via Helm on the lab OpenShift cluster and upserts the **OpenFlake** credential
- Portal auth is demo-grade (client-side AES-GCM unlock on a public S3 website). Object key is prefixed by the Gitea host so shared APD AWS accounts do not overwrite each other. Portal buckets (`apd-ss-portal-*`) are not deleted by cloud destroy workflows
- Kafka and other shared hosts can be added as parallel nodes later

## Related demos

| Demo | Description |
|------|-------------|
| [AWS Mattermost](./mattermost.md) | Standalone Mattermost provision |
| [AWS Gitea](./gitea.md) | Standalone Gitea provision |
| [OpenFlake](./openflake.md) | Standalone OpenFlake install / uninstall |
| [Deploy Cloud Stack in AWS](../../cloud/docs/deploy-cloud-stack.md) | Full stack including demo VMs |
| [Automation Orchestrator](./automation-orchestrator.md) | Path 2 step 2 — Shared Services before AO Install |

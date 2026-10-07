# AWS Mattermost

Stand up a shared Mattermost chat server on AWS for demos that post remediation or status notifications (Automation Orchestrator disk utilization, and other chat-backed demos later).

## Prerequisites

- **Deploy Cloud Stack in AWS** already run (VPC, subnet, security group, keypair)
- **AWS** and **APD Machine Credential** configured
- Sync **AWS Inventory** after this job so `aws_mattermost` appears in inventory

## Configure credentials

| Credential | Type | Notes |
|------------|------|-------|
| AWS | Amazon Web Services | EC2 create + security group |
| APD Machine Credential | Machine | SSH as `ec2-user` to configure Podman |
| AAP Credential | Red Hat Ansible Automation Platform | Lets this job upsert the **Mattermost** custom credential |

The playbook creates/updates a **Mattermost** custom credential (`mattermost_server` + incoming webhook id as `api_chat_token`) that other job templates attach. AO Install attaches it to **Notify Chatroom** and sets that JT to **Product Demos EE** (includes `community.general.mattermost`).

## Survey prompts

| Prompt | Variable | Default |
|--------|----------|---------|
| AWS Region | `create_vm_aws_region` | `us-east-2` |
| Owner | `create_vm_aws_owner_tag` | `your_name` (must match cloud stack owner tag) |
| Environment | `create_vm_vm_environment` | `Prod` |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Infrastructure ǀ AWS - Provision Mattermost | [`infrastructure/mattermost/provision_mattermost.yml`](../mattermost/provision_mattermost.yml) | EC2 `aws_mattermost` + Podman Postgres/Mattermost + admin/bot token |

## Why it matters

- One reusable chat endpoint for AO and other demos instead of hard-coded bastion IPs
- Bot token stored in the **Mattermost** Controller credential (injects `mattermost_server` / `api_chat_token`)
- Same cloud networking pattern as **Provision Kafka Queue** / Palo Alto credential write-back

## Presenter walkthrough

1. Run **Deploy Cloud Stack in AWS** (or reuse an existing stack)
2. Launch **Infrastructure ǀ AWS - Provision Mattermost** with the same region and owner tag
3. Confirm job output shows the **Mattermost** Controller credential was updated
4. Sync **AWS Inventory**
5. For AO demos: run **Infrastructure ǀ Automation Orchestrator ǀ Install** so **Notify Chatroom** gets the Mattermost credential attached

Default admin login is `apdadmin` / `Ansible123!` (username `admin` is reserved by Mattermost). Change it for long-lived labs.

## Talking points

- Mattermost runs as Podman containers (Postgres + team edition) on a dedicated RHEL 9 EC2 host
- Port **8065** is opened on `aws-test-sg` and firewalld
- Connection details are also written to `/etc/apd-mattermost.env` on the host

## Related demos

| Demo | Description |
|------|-------------|
| [Automation Orchestrator — Provisioning](./automation-orchestrator.md) | Install seeds demos that notify via Mattermost |
| [Config Drift — Kafka Queue](./config-drift-kafka.md) | Sibling AWS service host pattern (`aws_kafka`) |

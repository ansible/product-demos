# Deploy Cloud Stack in AWS


Provisions the full demo infrastructure in AWS: VPC, keypair, five VMs (two Windows, two RHEL, one reports server), dynamic inventory sync, and a VPC report published to S3. This is the starting point for most cloud, Linux, and Windows demos.

## Prerequisites

- <strong>If using RHDP (demo.redhat.com):</strong> Run <strong>APD | Multi-demo setup</strong> to configure all templates and credentials. AWS and APD Machine credentials are pre-configured for you.
- <strong>If using your own installation:</strong> Run <strong>APD | Single demo setup</strong> and choose <code>cloud</code>. Configure the <strong>AWS</strong> credential with your Access Key and Secret Key, and add an SSH private key to <strong>APD Machine Credential</strong>.

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| AWS Region | `aws_region` | multiplechoice | Yes |
| Owner | `owner_tag` | text | Yes |
| Environment | `env` | multiplechoice | Yes |
| Email | `email` | text | Yes |

## Why it matters

- Creates a complete demo environment in minutes — no manual AWS console clicking
- Configuration-as-code for infrastructure — the entire stack is defined in playbooks and blueprints
- Mixed OS fleet (RHEL 8, RHEL 9, Windows Server) reflects real customer environments
- Dynamic inventory automatically imports all provisioned VMs into AAP

## Presenter walkthrough

1. <strong>Show the survey:</strong> Walk through each field — region, owner, environment. Explain how surveys make self-service provisioning safe.
2. <strong>Launch:</strong> Start the workflow. As nodes light up, explain the sequence: keypair → VPC → parallel VM creation → inventory sync.
3. <strong>Parallel VM creation:</strong> Point out that all five VMs deploy simultaneously. 'This is the power of workflow nodes — parallel execution with dependency management.'
4. <strong>Inventory sync:</strong> After VMs are created, the dynamic inventory syncs automatically. Show the new hosts appearing in AAP.
5. <strong>VPC report:</strong> Show the S3 report — a visual summary of what was built.
6. <strong>Transition:</strong> 'Now that we have infrastructure, let's do something with it' — pivot to patching, compliance, or other demos.

## Related demos

| Demo | Description |
|------|-------------|
| 🩹 [Patch Cloud Stack in AWS](/product-demos/demos/patch-cloud-stack/) | Run this after deploying to demonstrate day-2 patching |
| 💥 [Destroy Cloud Stack in AWS](/product-demos/demos/cloud-destroy-stack/) | Tear down everything when done |
| 🐧 [Fact Scan](/product-demos/demos/linux-fact-scan/) | Gather facts from the newly deployed RHEL hosts |

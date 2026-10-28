# Add SSH Public Key


Adds your SSH public key to a Linux user's `authorized_keys` file on one or more hosts. Paste an Ed25519, RSA, or ECDSA public key in the survey to enable manual SSH access without logging in as root on each box or recovering the private key stored in **APD Machine Credential**.

This job is idempotent: re-running with the same key does not create duplicates.

## Prerequisites

- Linux hosts in the **Ansible Product Demos Inventory**
- SSH connectivity via **APD Machine Credential** (Ansible still needs an existing path in to run the job)
- The target user must exist on the system (for example, `ec2-user` on RHEL EC2 instances from [Deploy Cloud Stack in AWS](../../cloud/docs/deploy-cloud-stack.md))

## Survey prompts

| Prompt | Variable | Type | Required | Default | Description |
|--------|----------|------|----------|---------|-------------|
| Server Name or Pattern | `_hosts` | text | Yes | | Limit or pattern, for example `aws_rhel9` or `aws_rhel*` |
| SSH User | `ssh_user` | text | Yes | `ec2-user` | Linux account that receives the key |
| SSH Public Key | `ssh_public_key` | textarea | Yes | | Full public key line from `cat ~/.ssh/id_ed25519.pub` |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Add SSH Public Key | [`linux/install_ssh_key.yml`](../install_ssh_key.yml) | Adds the survey public key to the target user's `authorized_keys` file |

## Why it matters

- **APD Machine Credential** stores a private key for Ansible automation, but AAP does not let you export it after save
- Operators often want their **own** key for interactive SSH during demos, troubleshooting, or presenter prep
- Survey-driven, RBAC-controlled access beats ad-hoc `authorized_keys` edits on every host
- Works across host patterns (`aws_rhel*`) so one launch updates every matching RHEL worker

## Presenter walkthrough

1. **Generate a key (if needed):** `ssh-keygen -t ed25519 -f ~/.ssh/apd-demo -N ""`
2. **Copy the public key:** `cat ~/.ssh/apd-demo.pub`
3. **Launch the job:** Set `_hosts` to `aws_rhel*` (or a single host), leave **SSH User** as `ec2-user`, paste the public key
4. **Verify:** `ssh -i ~/.ssh/apd-demo ec2-user@<instance-ip>`
5. **Call out:** This adds your key alongside the cloud stack keypair; it does not replace **APD Machine Credential**

## Talking points

- Ed25519, RSA, and other standard OpenSSH public key formats are supported
- The playbook uses `ansible.posix.authorized_key` with `exclusive: false`, so existing keys (including `aws-test-key`) remain
- Same pattern customers use for onboarding operators onto fleets without sharing one break-glass credential

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](../../cloud/docs/deploy-cloud-stack.md) | Provisions the demo EC2 hosts this job is commonly run against |
| 🐧 [Troubleshoot](./linux-troubleshoot.md) | Investigate hosts after you SSH in manually |
| 🐧 [Run Shell Script](./linux-run-shell-script.md) | Run ad-hoc commands via AAP instead of SSH |

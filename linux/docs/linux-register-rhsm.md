# Register RHEL with RHSM


Registers RHEL hosts with Red Hat Subscription Manager using an activation key and org ID from the **RHSM Registration** credential. Uses the same registration logic as the patch cloud stack demos.

## Prerequisites

- RHEL hosts in the **Ansible Product Demos Inventory** (for example `aws_rhel9` from Deploy Cloud Stack in AWS)
- SSH connectivity via **APD Machine Credential**
- **RHSM Registration** credential with your Red Hat org ID and activation key — created by **APD ǀ Single demo setup** (`cloud` or `linux`). Replace `REPLACEME` values in AAP under Resources → Credentials → `RHSM Registration`. Create an activation key at [console.redhat.com](https://console.redhat.com/insights/connector/activation-key).

## Survey prompts

| Prompt | Variable | Type | Default | Description |
|--------|----------|------|---------|-------------|
| Server Name or Pattern | `_hosts` | text | `aws_rhel9` | `aws_rhel9` for one host, or `aws_rhel*` for every RHEL worker VM |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Register RHEL with RHSM | [`linux/register_rhsm.yml`](../register_rhsm.yml) | Registers unregistered RHEL hosts via activation key; no patching or Insights setup |

## Related demos

| Demo | Description |
|------|-------------|
| 🩹 [Patch Cloud Stack in AWS](../../cloud/docs/patch-cloud-stack.md) | Runs the same registration step automatically before RHEL patch jobs |
| 🔄 [Config Drift Remediation](../../infrastructure/docs/config-drift.md) | Run this before deploying Filebeat if `dnf` fails on unregistered hosts |

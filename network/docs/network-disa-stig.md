# DISA STIG


Applies DISA STIG compliance checks and hardening to Cisco IOS-XE network devices. Uses the demo.compliance.iosxeSTIG role to evaluate and enforce security controls for network infrastructure.

## Prerequisites

- Containerlab stack deployed via the **NETWORK ǀ Deploy Containerlab Stack** workflow
- **Containerlab Device Access** credential configured
- ContainerLab Inventory synced with hypervisor IP

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| What IOS-XE devices do you want to check? | `_hosts` | multiplechoice | Yes |

Options: `clab_ios` (default), `cat8kv`

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ DISA STIG | [`network/compliance.yml`](../compliance.yml) | Runs DISA STIG compliance checks and hardening on IOS-XE devices |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [DISA STIG](../../linux/docs/linux-disa-stig.md) | DISA STIG hardening for RHEL servers |
| 🪟 [DISA STIG](../../windows/docs/windows-disa-stig.md) | DISA STIG hardening for Windows servers |

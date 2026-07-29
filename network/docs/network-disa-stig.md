# DISA STIG


Applies DISA STIG compliance checks and hardening to Cisco IOS-XE network devices. Uses the demo.compliance.iosxeSTIG role to evaluate and enforce security controls for network infrastructure.

## Prerequisites

- Cisco IOS-XE devices in inventory
- Network credentials configured

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ DISA STIG | [`network/compliance.yml`](../compliance.yml) | Runs DISA STIG compliance checks and hardening on IOS-XE devices |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [DISA STIG](../../linux/docs/linux-disa-stig.md) | DISA STIG hardening for RHEL servers |
| 🪟 [DISA STIG](../../windows/docs/windows-disa-stig.md) | DISA STIG hardening for Windows servers |

# DISA STIG


Applies DISA STIG hardening to Windows Server 2022. Uses the demo.compliance.win2022STIG role to configure security controls required for U.S. Department of Defense Windows environments.

## Prerequisites

- Windows Server 2022 hosts in the <strong>Ansible Product Demos Inventory</strong>
- WinRM connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `HOSTS` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ DISA STIG | [`windows/compliance.yml`](../compliance.yml) | Applies Windows 2022 DISA STIG hardening controls from the demo.compliance collection |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [DISA STIG](../../linux/docs/linux-disa-stig.md) | DISA STIG hardening for RHEL servers |
| 🪟 [Configure Password Requirements](./windows-password-requirements.md) | Lighter-weight password policy configuration via DSC |

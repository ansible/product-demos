# Configure Password Requirements


Configures Windows password policies using PowerShell Desired State Configuration (DSC). Sets password history, minimum length, and complexity requirements. Demonstrates the integration of Ansible with Windows DSC.

## Prerequisites

- Windows hosts in the **Ansible Product Demos Inventory**
- WinRM connectivity via **APD Machine Credential**


## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | No |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Configure Password Requirements | [`windows/powershell_dsc.yml`](../powershell_dsc.yml) | Installs SecurityPolicyDSC module and configures password history, length, and complexity via DSC |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [DISA STIG](./windows-disa-stig.md) | Full STIG hardening which includes password policies and more |

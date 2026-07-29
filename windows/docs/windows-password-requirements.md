# Configure Password Requirements


Configures Windows password policies using PowerShell Desired State Configuration (DSC). Sets password history, minimum length, and complexity requirements. Demonstrates the integration of Ansible with Windows DSC.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong>
- WinRM connectivity via <strong>APD Machine Credential</strong>

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Configure Password Requirements | [`windows/powershell_dsc.yml`](https://github.com/ansible/product-demos/blob/main/windows/powershell_dsc.yml) | Installs SecurityPolicyDSC module and configures password history, length, and complexity via DSC |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [DISA STIG](/product-demos/demos/windows-disa-stig/) | Full STIG hardening which includes password policies and more |

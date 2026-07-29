# Query Services


Copies a PowerShell script to the target host and queries Windows services filtered by state (Running, Stopped, etc.). Demonstrates file transfer and script execution patterns on Windows with Ansible.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong>
- WinRM connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Service State | `service_state` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Query Services | [`windows/powershell_script.yml`](https://github.com/ansible/product-demos/blob/main/windows/powershell_script.yml) | Copies and runs a PowerShell script that filters services by the selected state |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Run PowerShell](/product-demos/demos/windows-run-powershell/) | Run arbitrary PowerShell for more complex queries |

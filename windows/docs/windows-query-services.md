# Query Services


Copies a PowerShell script to the target host and queries Windows services filtered by state (Running, Stopped, etc.). Demonstrates file transfer and script execution patterns on Windows with Ansible.

## Prerequisites

- Windows hosts in the **Ansible Product Demos Inventory**
- WinRM connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Service State | `service_state` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Query Services | [`windows/powershell_script.yml`](../powershell_script.yml) | Copies and runs a PowerShell script that filters services by the selected state |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Run PowerShell](./windows-run-powershell.md) | Run arbitrary PowerShell for more complex queries |

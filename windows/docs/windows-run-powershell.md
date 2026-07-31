# Run PowerShell


Runs an arbitrary PowerShell script on target Windows hosts. The script content is provided via survey. Outputs the results in the job log. Demonstrates how Ansible can execute any PowerShell command remotely.

## Prerequisites

- Windows hosts in the **Ansible Product Demos Inventory**
- WinRM connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| PowerShell Script | `ps_script` | textarea | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Run PowerShell | [`windows/powershell.yml`](../powershell.yml) | Executes the provided PowerShell script on target hosts and displays the output |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Run PowerShell (Kerberos)](./windows-run-powershell-kerberos.md) | Same playbook but with Kerberos authentication |
| 🪟 [Query Services](./windows-query-services.md) | Pre-built PowerShell script for querying services |

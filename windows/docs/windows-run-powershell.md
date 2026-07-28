---
layout: demo-detail
demo_slug: windows-run-powershell
---

Runs an arbitrary PowerShell script on target Windows hosts. The script content is provided via survey. Outputs the results in the job log. Demonstrates how Ansible can execute any PowerShell command remotely.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong>
- WinRM connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| PowerShell Script | `ps_script` | textarea | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS | Run PowerShell | [`windows/powershell.yml`](https://github.com/ansible/product-demos/blob/main/windows/powershell.yml) | Executes the provided PowerShell script on target hosts and displays the output |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Run PowerShell (Kerberos)](/product-demos/demos/windows-run-powershell-kerberos/) | Same playbook but with Kerberos authentication |
| 🪟 [Query Services](/product-demos/demos/windows-query-services/) | Pre-built PowerShell script for querying services |

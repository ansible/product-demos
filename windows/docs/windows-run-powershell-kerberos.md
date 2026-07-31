# Run PowerShell (Kerberos)


Runs a PowerShell script on Windows hosts using Kerberos authentication instead of basic WinRM. Demonstrates Ansible ability to authenticate via Active Directory credentials for domain-joined environments.

## Prerequisites

- Windows hosts joined to an Active Directory domain
- Kerberos credential configured in AAP
- Domain controller reachable from AAP

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| PowerShell Script | `ps_script` | textarea | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Run PowerShell ǀ Kerberos | [`windows/powershell.yml`](../powershell.yml) | Executes PowerShell on target hosts using Kerberos authentication |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Run PowerShell](./windows-run-powershell.md) | Same playbook with standard WinRM authentication |
| 🪟 [Setup Active Directory Domain](./windows-setup-ad-domain.md) | Set up an AD domain for Kerberos authentication |

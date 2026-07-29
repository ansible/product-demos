# AD — Create Domain


Promotes a Windows Server to a domain controller and creates a new Active Directory forest. Sets the local admin password, updates the hostname, creates the domain, and reboots. The default domain is ansible.local.

## Prerequisites

- A Windows Server VM not yet joined to a domain
- WinRM connectivity via <strong>APD Machine Credential</strong>


## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | No |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ AD ǀ Create Domain | [`windows/create_ad_domain.yml`](../create_ad_domain.yml) | Sets admin password, updates hostname, creates AD forest, and reboots |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [AD — Join Domain](./windows-ad-join-domain.md) | Join additional hosts to the domain after creation |
| 🪟 [Setup Active Directory Domain](./windows-setup-ad-domain.md) | Full workflow that automates the entire AD setup |

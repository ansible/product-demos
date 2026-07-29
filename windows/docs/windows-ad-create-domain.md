# AD — Create Domain


Promotes a Windows Server to a domain controller and creates a new Active Directory forest. Sets the local admin password, updates the hostname, creates the domain, and reboots. The default domain is ansible.local.

## Prerequisites

- A Windows Server VM not yet joined to a domain
- WinRM connectivity via <strong>APD Machine Credential</strong>

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ AD ǀ Create Domain | [`windows/create_ad_domain.yml`](https://github.com/ansible/product-demos/blob/main/windows/create_ad_domain.yml) | Sets admin password, updates hostname, creates AD forest, and reboots |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [AD — Join Domain](/product-demos/demos/windows-ad-join-domain/) | Join additional hosts to the domain after creation |
| 🪟 [Setup Active Directory Domain](/product-demos/demos/windows-setup-ad-domain/) | Full workflow that automates the entire AD setup |

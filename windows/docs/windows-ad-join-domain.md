# AD — Join Domain


Joins Windows hosts to an existing Active Directory domain. Sets the DNS client to point at the domain controller, creates an OU, updates the hostname, and performs the domain join.

## Prerequisites

- An existing AD domain (created by <strong>WINDOWS | AD | Create Domain</strong>)
- Domain controller private IP accessible from target hosts


## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Domain Controller Inventory Hostname | `domain_controller` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ AD ǀ Join Domain | [`windows/join_ad_domain.yml`](https://github.com/ansible/product-demos/blob/main/windows/join_ad_domain.yml) | Configures DNS, creates OU, updates hostname, and joins the host to the domain |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [AD — Create Domain](/product-demos/demos/windows-ad-create-domain/) | Create the domain before joining hosts |
| 🪟 [AD — New User](/product-demos/demos/windows-ad-new-user/) | Create users in the domain after hosts are joined |

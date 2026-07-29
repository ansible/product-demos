# AD — New User


Creates a new Active Directory user with full attributes -- name, department, company, address, phone, and group memberships. Generates a random temporary password. Demonstrates a helpdesk self-service portal for user provisioning.

## Prerequisites

- An Active Directory domain (deployed by **Setup Active Directory Domain** workflow)
- Domain controller accessible via WinRM

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| First Name | `firstname` | text | Yes |
| Surname | `surname` | text | Yes |
| Street | `street` | text | Yes |
| City | `city` | text | Yes |
| Postal Code | `postal_code` | text | Yes |
| Telephone | `telephone_number` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ AD ǀ New User | [`windows/helpdesk_new_user_portal.yml`](../helpdesk_new_user_portal.yml) | Creates an AD user with full attributes, random password, and group memberships |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Setup Active Directory Domain](./windows-setup-ad-domain.md) | Set up the AD domain before creating users |
| 🪟 [Run PowerShell](./windows-run-powershell.md) | Query AD for the newly created user |

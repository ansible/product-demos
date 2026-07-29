# Rollback


A generic rollback playbook used as a cleanup step in Windows workflows. Outputs a configurable rollback message. Used by the Setup Active Directory Domain workflow as the failure handler to clean up resources on error.

## Prerequisites

- Windows hosts in the **Ansible Product Demos Inventory**


## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | No |
| Rollback Message | `rollback_msg` | text | No |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Rollback | [`windows/rollback.yml`](../rollback.yml) | Outputs rollback message -- used as a failure handler in workflows |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Setup Active Directory Domain](./windows-setup-ad-domain.md) | Uses this playbook as its failure cleanup handler |

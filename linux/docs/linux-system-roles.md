---
layout: demo-detail
demo_slug: linux-system-roles
---
# System Roles


Applies one or more RHEL System Roles to target hosts. System Roles are a collection of Ansible roles for configuring common RHEL subsystems (timesync, network, storage, etc.) in a consistent, supported way.

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| System Roles | `system_roles` | multiselect | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ System Roles | [`linux/system_roles.yml`](https://github.com/ansible/product-demos/blob/main/linux/system_roles.yml) | Applies selected RHEL System Roles (timesync, network, storage, etc.) to target hosts |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Install Web Console (Cockpit)](/product-demos/demos/linux-cockpit/) | Install Cockpit web console using System Roles |

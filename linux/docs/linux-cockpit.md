---
layout: demo-detail
demo_slug: linux-cockpit
---
# Install Web Console (Cockpit)


Installs and configures the Cockpit web console on RHEL hosts using RHEL System Roles. Cockpit provides a browser-based management interface for Linux servers. Demonstrates how System Roles make complex configurations repeatable.

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Cockpit | [`linux/system_roles.yml`](https://github.com/ansible/product-demos/blob/main/linux/system_roles.yml) | Applies the cockpit System Role to install and configure the web console |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [System Roles](/product-demos/demos/linux-system-roles/) | Apply additional System Roles alongside Cockpit |

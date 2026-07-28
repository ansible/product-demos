---
layout: demo-detail
demo_slug: linux-temporary-sudo
---

Grants temporary sudo access to a user for a configurable duration. Creates a sudoers rule, schedules automatic cleanup via the at daemon, and removes the rule when time expires. Demonstrates just-in-time privilege escalation.

## Prerequisites

- Linux hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>
- The target user must exist on the system

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Sudo User | `sudo_user` | text | Yes |
| Time | `sudo_time` | integer | Yes |
| Time Units | `sudo_units` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX | Temporary Sudo | [`linux/temp_sudo.yml`](https://github.com/ansible/product-demos/blob/main/linux/temp_sudo.yml) | Creates a time-limited sudoers rule and schedules automatic cleanup |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Run Shell Script](/product-demos/demos/linux-run-shell-script/) | Run scripts that may need the temporary privileges |

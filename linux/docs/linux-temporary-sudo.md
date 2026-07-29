# Temporary Sudo


Grants temporary sudo access to a user for a configurable duration. Creates a sudoers rule, schedules automatic cleanup via the at daemon, and removes the rule when time expires. Demonstrates just-in-time privilege escalation.

## Prerequisites

- Linux hosts in the **Ansible Product Demos Inventory**
- SSH connectivity via **APD Machine Credential**
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
| LINUX ǀ Temporary Sudo | [`linux/temp_sudo.yml`](../temp_sudo.yml) | Creates a time-limited sudoers rule and schedules automatic cleanup |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Run Shell Script](./linux-run-shell-script.md) | Run scripts that may need the temporary privileges |

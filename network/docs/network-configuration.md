# Golden Configuration


Deploys golden configurations to Cisco IOS, IOS-XR, and NX-OS network devices using Ansible resource modules. Pulls configurations from a separate Git repository (Network Golden Configs) and applies them to the network devices.

## Prerequisites

- Network devices in inventory (Cisco IOS, IOS-XR, and/or NX-OS)
- Network credentials configured
- Run **APD | Single demo setup** with `network`

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK | Configuration | `(Network Golden Configs project)` | Applies golden configurations to network devices using Ansible resource modules |

## Related demos

| Demo | Description |
|------|-------------|
| 🌐 [Report](./network-report.md) | Generate a network report after applying configurations |
| 🌐 [Backup](./network-backup.md) | Back up device configs before making changes |

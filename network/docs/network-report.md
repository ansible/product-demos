# Report


Gathers facts from containerlab Cisco NX-OS and IOS-XE devices and displays a summary of each device including hostname, OS version, model, serial number, and interface addresses.

## Prerequisites

- Containerlab stack deployed via the **NETWORK | Deploy Containerlab Stack** workflow
- **Containerlab Device Access** credential configured
- ContainerLab Inventory synced with hypervisor IP

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| What devices do you want to include in the report? | `_hosts` | multiplechoice | Yes |

Options: `containerlab` (all devices), `clab_nxos`, `clab_ios`

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ Report | [`network/report.yml`](../report.yml) | Gathers facts from containerlab Cisco NX-OS and IOS-XE devices and displays a device summary |

## Related demos

| Demo | Description |
|------|-------------|
| 🌐 [Configure Devices](./network-configuration.md) | Apply baseline configurations before generating a report |
| 🌐 [Backup](./network-backup.md) | Back up configurations alongside reporting |

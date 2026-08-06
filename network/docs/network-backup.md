# Backup


Backs up running configurations from containerlab NX-OS and IOS-XE devices using the native `cisco.ios.ios_config` and `cisco.nxos.nxos_config` modules. Backup files are saved to the execution node.

## Prerequisites

- Containerlab stack deployed via the **NETWORK | Deploy Containerlab Stack** workflow
- **Containerlab Device Access** credential configured
- ContainerLab Inventory synced with hypervisor IP

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ Backup | [`network/backup.yml`](../backup.yml) | Backs up running configurations from containerlab network devices to the execution node |

## Related demos

| Demo | Description |
|------|-------------|
| 🌐 [Configure Devices](./network-configuration.md) | Apply configurations that you may want to back up first |
| 🌐 [Report](./network-report.md) | Generate a device report alongside backups |

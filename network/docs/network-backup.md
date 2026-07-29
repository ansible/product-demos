# Backup


Backs up running configurations from network devices to a report server. Sets up a backup directory on the report server, then saves device configs. Provides a browsable backup archive via HTTP.

## Prerequisites

- Network devices (routers) in inventory
- A <code>reports</code> host for storing backups
- Network credentials configured

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ Backup | [`network/backup.yml`](../backup.yml) | Sets up a backup directory on the report server and saves device running configs |

## Related demos

| Demo | Description |
|------|-------------|
| 🌐 [Golden Configuration](./network-configuration.md) | Apply configurations that you may want to back up first |
| 🌐 [Report](./network-report.md) | Generate a report alongside backups |

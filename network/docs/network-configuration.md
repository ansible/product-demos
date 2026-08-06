# Configure Devices


Applies baseline configuration to containerlab network devices (Cisco NX-OS and IOS-XE) using Ansible Network Resource Modules. Configures banners, NTP servers, and SNMP settings to demonstrate how Ansible standardizes configuration across different network operating systems.

## Prerequisites

- Containerlab stack deployed via the **NETWORK | Deploy Containerlab Stack** workflow
- **Containerlab Device Access** credential configured
- ContainerLab Inventory synced with hypervisor IP

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ Containerlab ǀ Configure Devices | [`network/configure_devices.yml`](../configure_devices.yml) | Applies banner, NTP, and SNMP configuration to containerlab NX-OS and IOS-XE devices |

## Why it matters

- Demonstrates Ansible Network Resource Modules applying the same logical configuration (NTP, SNMP, banners) across different Cisco platforms
- Shows how a single job template can configure heterogeneous network environments consistently
- Baseline configuration is a common first step before compliance checks or reporting

## Related demos

| Demo | Description |
|------|-------------|
| 🌐 [Report](./network-report.md) | Generate a device report after applying configurations |
| 🌐 [DISA STIG](./network-disa-stig.md) | Run compliance checks after establishing a baseline |
| 🌐 [Backup](./network-backup.md) | Back up device configs after making changes |

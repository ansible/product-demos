# Network Demo Guides

> **Full experience:** Browse the [GitHub Pages demo catalog](https://ipvsean.github.io/product-demos/) for workflow diagrams and search/filter.

## Workflows

| Demo | Description | Detail page |
|------|-------------|-------------|
| Palo Alto Firewall Demo | Deploy + configure PAN-OS | [Guide](https://ipvsean.github.io/product-demos/demos/network-panos-workflow/) |

## Standalone jobs

| Demo | Playbook | Description |
|------|----------|-------------|
| Golden Configuration | [setup.yml](../setup.yml) | ACL/BGP/OSPF/NTP/SNMP config |
| Report | [report.yml](../report.yml) | Network device facts HTML report |
| DISA STIG | [compliance.yml](../compliance.yml) | Network device compliance |
| Backup | [backup.yml](../backup.yml) | Config backup and reporting |

## Quick start

1. Run the **APD | Single demo setup** job template and select `network`
2. Ensure network device credentials are configured
3. For the Palo Alto demo, configure the **Panos** credential with PAN-OS credentials
4. Launch any network demo against your network inventory

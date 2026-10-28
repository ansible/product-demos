# Configure Devices

`network/configure_devices.yml` configures the connected `product_demos` lab through vendor network resource modules with `state: merged`. It uses **Containerlab Device Access** and **ContainerLab Inventory**. `_hosts` defaults to `containerlab` and can select a platform or device.

The `clab_junos` inventory group sets `ansible_netconf_port` to `ansible_port` so Junos modules that require either variable use the same mapped NETCONF port. Rerun Network setup to refresh this group on existing AAP instances.

## Routed topology

```mermaid
flowchart LR
  J[vjunos3] ---|10.10.13.0/30| C[cat8kv1]
  C ---|10.10.12.0/30| E[veos2]
  E ---|10.10.24.0/30| F[veos4]
```

| Node | Data interfaces and addresses | Loopback |
|---|---|---|
| `cat8kv1` | Gi2: 10.10.12.1/30; Gi3: 10.10.13.1/30 | Loopback10: 10.255.0.1/32 |
| `veos2` | Ethernet1: 10.10.12.2/30; Ethernet2: 10.10.24.1/30 | Loopback10: 10.255.0.2/32 |
| `vjunos3` | ge-0/0/0.0: 10.10.13.2/30 | lo0.0: 10.255.0.3/32 |
| `veos4` | Ethernet1: 10.10.24.2/30 | Loopback10: 10.255.0.4/32 |

Each device receives static routes to the other three loopbacks. This supports cross-vendor paths including vSRX → IOS-XE → EOS → EOS. Validation sources pings from loopback addresses so return traffic follows the configured routes. Management uses a separate interface. On vSRX, Configure Devices removes the image’s retained `mgmt_junos` instance and keeps its default gateway in the global table before applying routes; this avoids the pinned Juniper collection’s IPv4-only VRF parser defect. NETCONF reconnects after changing that context. Bootstrap [NETCONF client keepalives](https://www.juniper.net/documentation/us/en/software/junos/cli-reference/topics/ref/statement/ssh-edit-system-services-netconf.html) expire the disconnected server session so it releases its configuration lock before resource tasks continue.

Resource modules configure descriptions, routed interfaces, addressing, LLDP, NTP, and static routes. IOS-XE also receives the existing banner and SNMP baseline. EOS routing and vSRX NETCONF/security-zone ICMP access are enabled in bootstrap. A Junos security policy permits only `junos-icmp-ping` within the trust zone so packets can reach the loopback from the data interface. Junos logical interfaces omit the `enabled` field because the pinned resource module emits an invalid logical-interface statement for that field.

The IOS-XE SNMP community defaults to `apd-demo`, configurable through `network_lab_snmp_community`. Configuration removes the previous `public` community when migrating an existing lab. This is a demo baseline; SNMPv2c communities are not a substitute for authenticated production monitoring.

Bootstrap password hashes use the EOS-compatible SHA512 spelling with both Ansible hashing backends. Deployment validates the hash format before rendering credentials.

Configuration data lives in `demo.network.configure_lab` defaults. Junos static routes use their vendor-specific `next_hop` schema; IOS-XE and EOS use `next_hops`. Cisco/EOS changes are saved and Junos changes are committed by the resource modules.

Run **Configure Devices**, **Validate Devices**, then [**Report**](network-report.md). The validation job tests all four nodes and multi-hop forwarding. Rerun configuration after redeployment. When checking idempotence, compare actual before/after configuration as some modules reissue defaults and report changes.

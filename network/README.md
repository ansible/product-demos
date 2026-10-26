# Network Demos

The network demos show Ansible Automation Platform configuring and reporting on Cisco IOS-XE, Arista EOS, and Juniper Junos through their native Ansible collections. One connected Containerlab topology, `product_demos`, runs on an AWS EC2 hypervisor with nested virtualization.

## Connected lab

```mermaid
flowchart LR
  J[vjunos3 / vSRX] ---|ge-0/0/0 — Gi3| C[cat8kv1 / IOS-XE]
  C ---|Gi2 — Ethernet1| E[veos2 / EOS]
  E ---|Ethernet2 — Ethernet1| F[veos4 / EOS]
```

| Device | Kind / image | Management |
|---|---|---|
| `cat8kv1` | Catalyst 8000v / 17.13.01a | 172.20.20.12; SSH 2123 |
| `veos2` | Arista vEOS / 4.32.0F | 172.20.20.13; SSH 2124 |
| `vjunos3` | Juniper vSRX / 23.2R2.21 | 172.20.20.14; SSH 2125, NETCONF 2225 |
| `veos4` | Arista vEOS / 4.32.0F | 172.20.20.15; SSH 2126 |
| `scp-server` | Linux file server | 172.20.20.11 inside the lab |

Management IPs belong to the Containerlab network. AAP connects to device ports mapped on the hypervisor's public address. The **Containerlab Device Access** credential supplies authentication; Junos uses NETCONF and IOS-XE/EOS use `network_cli`. ContainerLab Inventory groups select all devices or a platform.

The topology uses the supplied IvyBridge CPU settings for both EOS nodes. The vSRX bootstrap enables NETCONF and allows ICMP to its demo interfaces. Configure Devices removes the image’s retained management VRF and preserves its gateway in the default routing table, because the pinned Juniper static-route parser fails on IPv4-only routing instances. NETCONF reconnects after that routing-context change. Device configuration adds routed links, loopbacks, LLDP, NTP, and static routes so demos can exercise paths across all three vendors.

## Getting started

**EE prerequisite:** Rebuild and publish Product Demos EE with this branch's collection and Python requirements, or use an accessible rebuilt EE until the official image is updated. A project sync does not update installed modules. See [EE prerequisites](../execution_environments/README.md#network-demo-testing-prerequisite).

1. Run APD setup and select **Network**.
2. Run **NETWORK | Deploy Containerlab Stack** to provision a hypervisor, deploy `product_demos`, and sync inventory. An existing hypervisor can use **NETWORK | Containerlab | Deploy Topology** directly.
3. Run **NETWORK | Containerlab | Configure Devices**.
4. Run **NETWORK | Containerlab | Validate Devices** to check structured collection and multi-hop pings sourced from each device's loopback.
5. Run **NETWORK | Report** and open its published HTML URL. Sanitized JSON is available beside it at `/network/report.json`.
6. When finished, run **NETWORK | Destroy Containerlab Stack** to remove the lab and AWS resources.

Deployment uses a single topology; no topology selection survey is needed. Redeploying resets all four devices to bootstrap. Older `product_demos` and `multi-vendor` deployments are stopped before the connected replacement is rendered, and retired inventory hosts are removed after successful deployment. Regenerate the report after deployment or teardown changes device membership.

## Job templates

| Template | Purpose |
|---|---|
| **Provision Hypervisor** | Create AWS networking, keys, and a RHEL 9 EC2 host with KVM; defaults to c8i.4xlarge. |
| **Deploy Topology** | Install Containerlab/Podman, pull images, render credentials, deploy the connected lab, refresh management ports, and update inventory. |
| **Configure Devices** | Merge vendor-native interface, address, LLDP, NTP, and route configuration; retain Cisco banner/SNMP baselines. |
| **Validate Devices** | Capture hypervisor/KVM/resource evidence, collect structured data, and test routed paths between vendors. |
| **Report** | Publish searchable HTML and sanitized JSON with identity, live interfaces, neighbors, configuration, and independent collection status. |
| **Backup** | Back up the IOS-XE configuration using the Cisco collection. |
| **DISA STIG** | Assess IOS-XE configuration in check mode by default. |
| **Staging / Upgrade** | Stage an IOS-XE image over SCP, then install and activate it; run Staging first. |
| **Troubleshoot** | Inspect management ports, the topology, host resources, and container logs. |
| **Teardown Topology** | Destroy the topology and remove its report while retaining the hypervisor. |
| **Teardown Hypervisor** | Remove the EC2 instance and associated AWS resources. |

Read [configuration](docs/network-configuration.md), [deployment](docs/network-deploy-containerlab-stack.md), [reporting](docs/network-report.md), and [troubleshooting](docs/network-troubleshoot-containerlab.md) for details. The [Palo Alto firewall demo](docs/network-panos-workflow.md) remains separate.

Configuration resources execute in each vendor's dependency order with `state: merged`. Some Cisco and EOS modules can report changes for defaults even when before/after values match; inspect configuration data when checking idempotence. The vSRX topology requires its own live validation; prior vJunos-switch or split-lab results do not establish compatibility for this image and layout.

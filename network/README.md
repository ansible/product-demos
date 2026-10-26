# Network Demos

## Table of Contents
- [Network Demos](#network-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
  - [Infrastructure](#infrastructure)
  - [Getting Started](#getting-started)
  - [Workflows](#workflows)
  - [Job Templates](#job-templates)
  - [Suggested Usage](#suggested-usage)

## About These Demos
This category of demos shows examples of network operations and management with Ansible Automation Platform. Choose the original `product_demos` lab with Cisco IOS-XE and NX-OS, or the `multi-vendor` lab with Juniper Junos and Arista EOS. Both run in a [containerlab](https://containerlab.dev/) topology on AWS, providing a fully self-contained environment with no external dependencies.

## Infrastructure

The network demos use containerlab to run virtual network devices as containers on an AWS EC2 hypervisor with nested virtualization enabled.

| Component | Details |
|-----------|---------|
| **Hypervisor** | RHEL 9 on AWS EC2 (c8i.4xlarge by default) with nested virtualization |
| **Container Runtime** | Podman |
| **NX-OS Device** | Cisco Nexus 9000v (`n9kv`) — SSH on port 2122 |
| **IOS-XE Device** | Cisco Catalyst 8000v (`cat8kv`) — SSH on port 2123 |
| **Junos Device** | `multi-vendor` only: Juniper vJunos-switch (`vjunos`) — SSH 2124, NETCONF 2830 |
| **EOS Device** | `multi-vendor` only: Arista vEOS (`veos`) — SSH 2125 |
| **Report** | Persistent HTML and sanitized JSON at `http://<hypervisor>:8088/network/` |
| **Regions** | us-east-2, us-west-2 |

Deploy Topology adds the selected lab on the existing hypervisor. `product_demos` owns the Cisco devices and SCP server; `multi-vendor` owns Junos and EOS with a link between them. Both labs can run together. Redeploying resets only the selected lab to bootstrap. Inventory enables devices from all deployed labs. Teardown can remove one lab or all labs, and Troubleshoot discovers all deployed topologies. The original `product_demos` topology and startup files are restored from `main`, including their `admin` / `admin@123` device credentials.

Devices use port-mapped management services on the hypervisor. The **Containerlab Device Access** credential supplies device authentication; Junos uses NETCONF and the other platforms use `network_cli`. A dedicated **ContainerLab Inventory** holds the device hosts and group variables.

## Getting Started

1. Deploy the demos using the "Product Demos | Multi-demo setup" or "Product Demos | Single demo setup" and select **Network**.
2. Run the **NETWORK ǀ Deploy Containerlab Stack** workflow to provision the infrastructure. This will:
   - Provision an EC2 hypervisor with nested virtualization
   - Deploy the topology selected in the survey: `product_demos` (default: n9kv + cat8kv) or `multi-vendor` (vjunos + veos)
   - Sync the ContainerLab Inventory with the hypervisor IP
3. To run both labs, launch **NETWORK ǀ Containerlab ǀ Deploy Topology** on the same hypervisor and select the other topology.
4. Run **Configure Devices**, then **Report**. For `multi-vendor`, run **Validate Devices** after configuration to check forwarding across the connected lab. The report job publishes a browser URL in its output and AAP artifacts. Cisco Backup, DISA STIG, Staging, and Upgrade remain available.
5. When finished, run **NETWORK ǀ Destroy Containerlab Stack** to tear down all AWS resources.

## Workflows

| Workflow | Description |
|----------|-------------|
| [**Deploy Containerlab Stack**](docs/network-deploy-containerlab-stack.md) | Provision an AWS hypervisor, deploy the containerlab topology, and sync the inventory. |
| [**Destroy Containerlab Stack**](docs/network-destroy-containerlab-stack.md) | Tear down the containerlab topology and delete all AWS resources (VPC, subnet, security group, EC2 instance, keypair). |
| [**Palo Alto Firewall Demo**](docs/network-panos-workflow.md) | End-to-end Palo Alto firewall workflow: deploy, configure, validate, and clean up a PAN-OS instance. |

## Job Templates

### Containerlab Lifecycle

| Job Template | Description |
|--------------|-------------|
| **Provision Hypervisor** | Create AWS VPC, subnet, security group, keypair, and launch a RHEL 9 EC2 instance with nested virtualization enabled. |
| **Deploy Topology** | Install podman and containerlab on the hypervisor, pull device images, and start the topology selected in the survey. |
| **Configure Devices** | Merge interface, VLAN, trunk, addressing, LLDP, and NTP configuration for deployed platforms; retain Cisco banner and SNMP baselines. |
| **Validate Devices** | For `multi-vendor`, check KVM, capacity, device facts, and configured data-path reachability. Starts with Junos to validate the new image on EC2. |
| **Teardown Topology** | Choose `product_demos`, `multi-vendor`, or `all`; other deployed labs remain running. |
| **Troubleshoot** | Collect hypervisor, containerlab, and podman diagnostics through AAP when manual SSH is unavailable. |
| **Teardown Hypervisor** | Terminate the EC2 instance and remove all associated AWS resources. |

### Demo Jobs

| Job Template | Description |
|--------------|-------------|
| **Report** | Publish a detailed multi-vendor web report with identity, operational interfaces, neighbors, structured configuration, and independent collection status. |
| **DISA STIG** | Run the DISA STIG role against the IOS-XE device to assess configuration compliance. Runs in check mode by default. |
| **Backup** | Back up running configurations from containerlab NX-OS and IOS-XE devices using native Cisco collection modules. |
| **Staging** | Stage a new IOS-XE image to the IOS-XE device bootflash via SCP, then verify the file integrity with a SHA-512 hash check. Must be run before **Upgrade**. |
| **Upgrade** | Install and activate the staged IOS-XE image, reload the device, and verify the new version is running. Requires **Staging** to have completed successfully first. |

### Palo Alto

| Job Template | Description |
|--------------|-------------|
| **Panos \| Deploy** | Deploy a PAN-OS firewall instance and web server on AWS. |
| **Panos \| Configure Firewall** | Configure the PAN-OS firewall with network and security settings. |
| **Panos \| Configure Security Rule** | Create or modify a security rule on the PAN-OS firewall. |
| **Panos \| Configure Webserver** | Configure the web server behind the firewall. |
| **Panos \| Cleanup** | Remove all Palo Alto demo AWS resources. |

## Suggested Usage

**Deploy the stack first** — Choose `product_demos` for the original Cisco demos or `multi-vendor` for the connected Juniper/Arista lab. Run the **NETWORK ǀ Deploy Containerlab Stack** workflow before any other network demo. The workflow provisions infrastructure and populates the ContainerLab Inventory. For `multi-vendor`, allow at least 15 minutes for vJunos boot plus image pulls. Per-device readiness timeouts include 30 minutes for Junos; EC2 boot timing is still to be measured.

**NETWORK ǀ Configure Devices** — Configure the deployed devices with vendor network resource modules and `state: merged`. The same logical network intent is expressed in each platform's structured schema.

**NETWORK ǀ Containerlab ǀ Validate Devices** — With `multi-vendor` deployed, validate device collection and cross-device pings after configuration. The job also records hypervisor KVM support and container resource usage. On October 22, 2026, all four devices were deployed and configured through APD on AAP 2.7 using `c8i.4xlarge` in `us-east-2`. The exact vJunos-switch `25.2R1.9` image passed its forwarding test on EC2. This is a functional validation; prolonged load and reboot stability remain unmeasured.

The tested deployment needs three compatibility settings included in this branch: vEOS masks the unsupported nested-KVM performance-capabilities feature with `QEMU_CPU=host,level=9,pdcm=off`; EOS password hashes use the standard SHA-512 format without a `rounds=` prefix; and the Junos interface intent omits the `enabled` field because `juniper.device` 2.0.1 emits invalid logical-interface statements. Configuration resources run independently per device to preserve each vendor's dependency order.

Repeated configuration succeeds, but current Cisco and EOS modules can reissue default settings and report changes despite identical before/after data. IOS-XE configuration saving also reports a change on repeated runs. Do not interpret the changed-task count alone as configuration drift.

**NETWORK ǀ Report** — Open the detailed HTML report linked in the job output and artifacts. Search or filter by vendor, expand resource configuration, and compare live interface and neighbor observations. See the [report guide](docs/network-report.md) for collection coverage and failure behavior. Rebuild the Product Demos EE before using the new modules.

**NETWORK ǀ DISA STIG** — Run in check mode (default) to show how Ansible assesses compliance against DISA STIG rules on IOS-XE devices. Click into tasks to see what would change for each compliance rule.

**NETWORK ǀ Backup** — Back up device configurations using the native `cisco.ios.ios_config` and `cisco.nxos.nxos_config` modules. Backups are saved on the execution node. This demonstrates how Ansible can automate configuration backup across heterogeneous network environments.

**NETWORK ǀ Staging** — Stage a new IOS-XE image onto the cat8kv device. Enables SCP on the IOS-XE device, transfers the image to bootflash, and verifies the file integrity with a SHA-512 hash check. This job must be run **before** the Upgrade job — the upgrade will fail if no image has been staged. The IOS version is selected via a survey (`image_staging`), and several variables are pre-configured in the job template extra variables (`scp_server`, `sha_hash`) and the SCP credential (`scp_user`, `scp_password`). The playbook derives `new_version` and `new_image_ios` automatically from the survey selection.

**NETWORK ǀ Upgrade** — Install and activate the previously staged IOS-XE image on the cat8kv device. The playbook sets the boot system to the new image, runs `install add activate commit`, waits for the device to reload, and then verifies the new version is running. **You must run Staging first** — the upgrade checks that the image exists in bootflash and will fail if it is missing. The IOS version is selected via a survey (`image_upgrade`), and the playbook derives `new_version` and `new_image_ios` automatically from the survey selection. Note: the upgrade and reboot process may take approximately 10 minutes to complete. Also in rare instances the reboot will show the original version if the router container fails and respawns during the reboot. Just run the upgrade again and it should be fine.

**NETWORK ǀ Panos** — See the [Palo Alto README](./panos/README.md) for usage instructions.

**Clean up when done** — Run the **NETWORK ǀ Destroy Containerlab Stack** workflow to remove all AWS resources and avoid unnecessary costs.

## Troubleshooting

### Receptor Pod Connection Refused

If a job fails with an error like:

```
Error with pod's stdout: Error getting pod aap/automation-job-XX-xxxxx.
Error: Get "https://172.231.0.1:443/api/v1/namespaces/aap/pods/automation-job-XX-xxxxx":
dial tcp 172.231.0.1:443: connect: connection refused
```

This means the execution environment pod lost connectivity to the Kubernetes API server. Common causes include API server pressure, node resource exhaustion, or network policies blocking egress from the `aap` namespace. Try relaunching the job template — if the error is intermittent it is usually transient and a relaunch will succeed. If it persists, check `oc get co`, `oc get nodes`, and `oc get networkpolicy -n aap` to verify the cluster and network are healthy.

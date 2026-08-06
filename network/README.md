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
This category of demos shows examples of network operations and management with Ansible Automation Platform. The demos run against Cisco NX-OS and IOS-XE devices hosted in a [containerlab](https://containerlab.dev/) topology on AWS, providing a fully self-contained environment with no external dependencies.

## Infrastructure

The network demos use containerlab to run virtual Cisco devices as containers on an AWS EC2 hypervisor with nested virtualization enabled.

| Component | Details |
|-----------|---------|
| **Hypervisor** | RHEL 9 on AWS EC2 (c8i.2xlarge) with nested virtualization |
| **Container Runtime** | Podman |
| **NX-OS Device** | Cisco Nexus 9000v (`n9kv`) — SSH on port 2122 |
| **IOS-XE Device** | Cisco Catalyst 8000v (`cat8kv`) — SSH on port 2123 |
| **Regions** | us-east-2, us-west-2 |

Device connectivity is handled via an **SSH Proxy** credential type that routes connections through the hypervisor to the containerlab devices. A dedicated **ContainerLab Inventory** holds the device hosts and group variables.

## Getting Started

1. Deploy the demos using the "Product Demos | Multi-demo setup" or "Product Demos | Single demo setup" and select **Network**.
2. Run the **NETWORK | Deploy Containerlab Stack** workflow to provision the infrastructure. This will:
   - Provision an EC2 hypervisor with nested virtualization
   - Deploy the containerlab topology (n9kv + cat8kv)
   - Sync the ContainerLab Inventory with the hypervisor IP
3. Once the stack is up, run the demo job templates (Report, Backup, DISA STIG, Configure Devices).
4. When finished, run **NETWORK | Destroy Containerlab Stack** to tear down all AWS resources.

## Workflows

| Workflow | Description |
|----------|-------------|
| [**Deploy Containerlab Stack**](#getting-started) | Provision an AWS hypervisor, deploy the containerlab topology, and sync the inventory. |
| [**Destroy Containerlab Stack**](#getting-started) | Tear down the containerlab topology and delete all AWS resources (VPC, subnet, security group, EC2 instance, keypair). |
| [**Palo Alto Firewall Demo**](docs/network-panos-workflow.md) | End-to-end Palo Alto firewall workflow: deploy, configure, validate, and clean up a PAN-OS instance. |

## Job Templates

### Containerlab Lifecycle

| Job Template | Description |
|--------------|-------------|
| **Provision Hypervisor** | Create AWS VPC, subnet, security group, keypair, and launch a RHEL 9 EC2 instance with nested virtualization enabled. |
| **Deploy Topology** | Install podman and containerlab on the hypervisor, pull device images, and start the n9kv + cat8kv topology. |
| **Configure Devices** | Apply baseline configuration (banner, NTP, SNMP) to the containerlab NX-OS and IOS-XE devices. |
| **Teardown Topology** | Destroy the running containerlab topology on the hypervisor. |
| **Teardown Hypervisor** | Terminate the EC2 instance and remove all associated AWS resources. |

### Demo Jobs

| Job Template | Description |
|--------------|-------------|
| **Report** | Gather facts from containerlab Cisco devices and display device information including hostname, OS version, model, serial number, and interfaces. |
| **DISA STIG** | Run the DISA STIG role against the IOS-XE device to assess configuration compliance. Runs in check mode by default. |
| **Backup** | Back up running configurations from containerlab NX-OS and IOS-XE devices using native Cisco collection modules. |

### Palo Alto

| Job Template | Description |
|--------------|-------------|
| **Panos \| Deploy** | Deploy a PAN-OS firewall instance and web server on AWS. |
| **Panos \| Configure Firewall** | Configure the PAN-OS firewall with network and security settings. |
| **Panos \| Configure Security Rule** | Create or modify a security rule on the PAN-OS firewall. |
| **Panos \| Configure Webserver** | Configure the web server behind the firewall. |
| **Panos \| Cleanup** | Remove all Palo Alto demo AWS resources. |

## Suggested Usage

**Deploy the stack first** — Run the **NETWORK | Deploy Containerlab Stack** workflow before any other network demo. The workflow provisions infrastructure and populates the ContainerLab Inventory. Provisioning takes approximately 10-15 minutes while device images are pulled and virtual devices boot.

**NETWORK | Configure Devices** — Run this after deploying the stack to apply baseline device configuration (NTP, SNMP, banners) using Cisco Network Resource Modules. This demonstrates how Ansible standardizes configuration across different network operating systems.

**NETWORK | Report** — Gather facts from the containerlab devices and display a summary of each device. Shows how Ansible can collect and present network device information for reporting and auditing.

**NETWORK | DISA STIG** — Run in check mode (default) to show how Ansible assesses compliance against DISA STIG rules on IOS-XE devices. Click into tasks to see what would change for each compliance rule.

**NETWORK | Backup** — Back up device configurations using the native `cisco.ios.ios_config` and `cisco.nxos.nxos_config` modules. Backups are saved on the execution node. This demonstrates how Ansible can automate configuration backup across heterogeneous network environments.

**NETWORK | Panos** — See the [Palo Alto README](./panos/README.md) for usage instructions.

**Clean up when done** — Run the **NETWORK | Destroy Containerlab Stack** workflow to remove all AWS resources and avoid unnecessary costs.

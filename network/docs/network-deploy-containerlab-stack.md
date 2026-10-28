# Deploy Containerlab Stack

Provision a nested-virtualization AWS hypervisor, deploy one connected `product_demos` topology, and sync ContainerLab Inventory. The topology contains `cat8kv1`, `veos2`, `vjunos3`, `veos4`, and an SCP server.

## Prerequisites

Run APD setup with **Network**, configure AWS/AAP credentials, and select a rebuilt Product Demos EE with the network requirements in this branch. The official EE needs rebuilding/publishing; a project sync alone does not install new modules.

## Survey

| Prompt | Variable | Choices |
|---|---|---|
| AWS Region | `clab_aws_region` | us-east-2 (default), us-west-2 |
| Instance Type | `clab_aws_instance_type` | c8i.4xlarge (default), c8i.2xlarge |
| Allowed management source CIDR | `clab_access_cidr` | IPv4 CIDR; defaults to `0.0.0.0/0` |
| Owner | `clab_aws_owner_tag` | Text |

Provision Hypervisor, Deploy Containerlab Stack, and standalone Deploy Topology ask for the allowed management source CIDR. Deploy Topology also asks for region. Both deployment entry points use `product_demos`; there is no topology choice.

## Capacity and cost

The default increases from `c8i.2xlarge` (8 vCPU, 16 GiB) to `c8i.4xlarge` (16 vCPU, 32 GiB). The connected lab runs four nested QEMU network VMs concurrently, plus the SCP container, host services, and report server. The larger size provides CPU and memory headroom during concurrent boot and collection; live acceptance used this size. It is the validated baseline, rather than a measured minimum requirement. The smaller survey choice remains available for capacity experiments and has not been validated for the complete four-device lab.

**This increases the default EC2 compute cost.** Check the current regional RHEL rate before launching; storage and public IPv4 charges are separate. See [AWS C8i specifications](https://aws.amazon.com/ec2/instance-types/compute-optimized/) and [EC2 pricing](https://aws.amazon.com/ec2/pricing/on-demand/). Destroy Containerlab Stack removes the EC2 instance and associated lab resources when the demo is finished.

## Management access

Choose a source CIDR that includes the AAP execution-node egress and presenter addresses. The survey retains `0.0.0.0/0` for existing workshop environments whose egress range is not known in advance, and provisioning/deployment prints a warning when this open scope is selected. That scope exposes hypervisor SSH, mapped device SSH/NETCONF, and the HTTP report publicly while the devices use demo credentials. Select a restricted CIDR for your environment; restricting it only to a presenter's address can prevent AAP from reaching the lab.

## Workflow

1. **Provision Hypervisor** creates AWS networking, keypair, storage, and EC2 host.
2. **Deploy Topology** enables KVM, installs Podman/Containerlab, pulls images, renders bootstrap credentials, starts all devices, waits for management services, configures persistent report hosting, and updates inventory.
3. **Sync ContainerLab Inventory** discovers the hypervisor for report and device jobs.

Run **Configure Devices**, **Validate Devices**, and **Report** afterward. Image pulls and virtual-device startup take time; readiness timeouts are 15 minutes for IOS-XE/EOS and 30 minutes for vSRX.

## Existing hypervisors and migration

Deploy Topology discovers the hypervisor by EC2 tags, or accepts `clab_host_ip`. It refreshes management rules for SSH, device ports 2123–2126, NETCONF 2225, and report HTTP 8088. `clab_access_cidr` controls the allowed source network.

The existing deployment record recognizes old `product_demos` and `multi-vendor` labs. Deployment destroys those labs using their existing topology files before rendering the connected replacement, freeing their ports and management IPs. A cleanup failure stops redeployment. The new inventory contains the four current node names; retired `n9kv`, `cat8kv`, `vjunos`, and `veos` hosts are removed after deployment succeeds.

Redeployment resets the whole lab to bootstrap. Teardown Topology removes the lab and report; Destroy Containerlab Stack also removes its AWS resources. Use [Troubleshoot](network-troubleshoot-containerlab.md) to collect boot, port, and container diagnostics when readiness fails.

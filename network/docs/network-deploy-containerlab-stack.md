# Deploy Containerlab Stack

Provision a nested-virtualization AWS hypervisor, deploy one connected `product_demos` topology, and sync ContainerLab Inventory. The topology contains `cat8kv1`, `veos2`, `vjunos3`, `veos4`, and an SCP server.

## Prerequisites

Run APD setup with **Network**, configure AWS/AAP credentials, and select a rebuilt Product Demos EE with the network requirements in this branch. The official EE needs rebuilding/publishing; a project sync alone does not install new modules.

## Survey

| Prompt | Variable | Choices |
|---|---|---|
| AWS Region | `clab_aws_region` | us-east-2 (default), us-west-2 |
| Instance Type | `clab_aws_instance_type` | c8i.4xlarge (default), c8i.2xlarge |
| Owner | `clab_aws_owner_tag` | Text |

The standalone Deploy Topology job asks only for region. Both entry points deploy `product_demos`; there is no topology choice.

## Workflow

1. **Provision Hypervisor** creates AWS networking, keypair, storage, and EC2 host.
2. **Deploy Topology** enables KVM, installs Podman/Containerlab, pulls images, renders bootstrap credentials, starts all devices, waits for management services, configures persistent report hosting, and updates inventory.
3. **Sync ContainerLab Inventory** discovers the hypervisor for report and device jobs.

Run **Configure Devices**, **Validate Devices**, and **Report** afterward. Image pulls and virtual-device startup take time; readiness timeouts are 15 minutes for IOS-XE/EOS and 30 minutes for vSRX.

## Existing hypervisors and migration

Deploy Topology discovers the hypervisor by EC2 tags, or accepts `clab_host_ip`. It refreshes management rules for SSH, device ports 2123–2126, NETCONF 2225, and report HTTP 8088. `clab_access_cidr` controls the allowed source network.

The existing deployment record recognizes old `product_demos` and `multi-vendor` labs. Deployment destroys those labs using their existing topology files before rendering the connected replacement, freeing their ports and management IPs. A cleanup failure stops redeployment. The new inventory contains the four current node names; retired `n9kv`, `cat8kv`, `vjunos`, and `veos` hosts are removed after deployment succeeds.

Redeployment resets the whole lab to bootstrap. Teardown Topology removes the lab and report; Destroy Containerlab Stack also removes its AWS resources. Use [Troubleshoot](network-troubleshoot-containerlab.md) to collect boot, port, and container diagnostics when readiness fails.

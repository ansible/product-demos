# Cloud Demo Guides

> **Full experience:** Browse the [GitHub Pages demo catalog](https://ipvsean.github.io/product-demos/) for workflow diagrams, presenter walkthroughs, and search/filter.

## Workflows

| Demo | Description | Detail page |
|------|-------------|-------------|
| [Deploy Cloud Stack in AWS](../setup.yml) | Provision VPC, keypair, and 5 VMs in one click | [Guide](https://ipvsean.github.io/product-demos/demos/deploy-cloud-stack/) |
| [Destroy Cloud Stack in AWS](../setup.yml) | Tear down the full stack | [Guide](https://ipvsean.github.io/product-demos/demos/cloud-destroy-stack/) |
| [Patch Cloud Stack in AWS](../setup.yml) | Snapshot, patch, verify, restore for RHEL + Windows | [Guide](https://ipvsean.github.io/product-demos/demos/patch-cloud-stack/) |

## Standalone jobs

| Demo | Playbook | Description |
|------|----------|-------------|
| AWS — Create VPC | [create_vpc.yml](../create_vpc.yml) | VPC with subnet, security group, route table |
| AWS — Create Keypair | [aws_key.yml](../aws_key.yml) | EC2 keypair from APD Machine Credential |
| AWS — Create VM | [create_vm.yml](../create_vm.yml) | EC2 instance from blueprint |
| AWS — Delete VM | [delete_vm_by_name.yml](../delete_vm_by_name.yml) | Terminate EC2 by Name tag |
| AWS — Resize EC2 | [resize_ec2.yml](../resize_ec2.yml) | Change instance type |
| AWS — Snapshot EC2 | [snapshot_ec2.yml](../snapshot_ec2.yml) | EBS snapshots for backup |
| AWS — Restore EC2 | [restore_ec2.yml](../restore_ec2.yml) | Volume restore from snapshot |

## Quick start

1. Run the **APD | Single demo setup** job template and select `cloud`
2. Configure the **AWS** credential with your Access Key and Secret Key
3. Add an SSH private key to **APD Machine Credential**
4. Launch **Deploy Cloud Stack in AWS** to create the demo environment
5. Run any other cloud demo against the provisioned infrastructure

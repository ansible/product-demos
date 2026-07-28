# Transit Network Deployment Role

This Ansible role contains repeatable automation for a hub-and-spoke VPC peering model that can help establish template infrastructure configurations that may be used for starting an AWS networking infrastructure strategy or to create demonstrations for network peering scenarios.

## Create Transit Network

This operation will create the resources necessary for a transit network model with two VPCs; one acting as a public internet-facing DMZ where bastion servers and other internet resources could exist, and another that acts as an entirely private network with no internet access.  These networks are configured with security groups and routing rules that allow traffic between the two VPCs and their subnets through the transit gateway.  Once deployed, you can SSH in to the bastion host in order to can access to the host on the private network.

### Variables

The following variables are used during deployment and can be configured as extra vars at deploy time if you require something other than the defaults.

#### Required

```yaml
---
aws_region: us-east-1 # The region in which the resources are deployed
dmz_ssh_key_name: aws-test-key # The AWS SSH key to use when configuring access to the EC2 instances on the DMZ network.
priv_network_ssh_key_name: aws-test-key # The AWS SSH key to use when configuring access to the EC2 instances on the private network.
ssh_key_data: lookup('file', '~/.ssh/aws-test-key.pem') # The contents of the AWS SSH private key to store on the DMZ server for access to private network servers
```

#### Optional

```yaml
---
# These variables can be configured to change the VPC networks and the EC2 instances deployed into them.
tenancy: default
vpc_priv_net_cidr: 10.0.0.0/16
vpc_priv_net_priv_subnet_cidr: 10.0.0.0/24
vpc_priv_net_hosts_pattern: 10.0.*
vpc_dmz_cidr: 10.1.0.0/16
vpc_dmz_subnet1_cidr: 10.1.0.0/24
dmz_instance_type: t2.micro
dmz_instance_name: dmz-ssh-tunnel-vm
dmz_instance_ami_owner: "{{ omit }}"
dmz_instance_ami_architecture: x86_64
dmz_instance_ami_filter: RHEL-8*HVM-*Hourly*
dmz_instance_ami: undef # use this variable to override the AMI lookup
priv_network_instance_type: t2.micro
priv_network_instance_name: priv-network-vm
priv_network_instance_ami_owner: "{{ omit }}"
priv_network_instance_ami_architecture: x86_64
priv_network_instance_ami_filter: RHEL-8*HVM-*Hourly*
priv_network_instance_name: priv-network-vm
priv_natwork_instance_ami: undef # use this variable to override the AMI lookup
ansible_ssh_private_key_file_local_path: ~/.ssh/aws-test-key.pem # Must exist locally or be mapped in an EE
ansible_ssh_private_key_file_dest_path: ~/.ssh/aws-test-key.pem
priv_network_ssh_user: ec2-user

```

### Infrastructure

The following AWS infrastructure resources are created during this deployment.  Each resource is configured with a set of tags that are used to determine if resources already exist, and which resources to clean up if the `delete` operation is run.

### Architecture Diagram

![Deployment Architecture Diagram](./files/transit_network_arch_diagram.png)

Resources below the dotted line demonstrate how you may connect other resources to the VPCs through a transit gateway attachment.

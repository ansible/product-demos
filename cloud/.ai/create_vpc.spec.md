# create_vpc.yml

## Purpose
Provisions core AWS networking resources for the cloud demo, then publishes key network identifiers as runtime stats.

## Execution Context
- Runs on `localhost`.
- `gather_facts` is disabled.
- Requires AWS credentials/config and a valid `create_vm_aws_region`.

## Workflow
1. Creates a VPC (`amazon.aws.ec2_vpc_net`).
2. Creates and attaches an internet gateway (`amazon.aws.ec2_vpc_igw`).
3. Creates a security group (`amazon.aws.ec2_security_group`) with ingress/egress rules for demo workloads.
4. Creates a public subnet (`amazon.aws.ec2_vpc_subnet`) in a shuffled AZ from the per-region `_azs` map.
5. Creates a route table and default route through the internet gateway (`amazon.aws.ec2_vpc_route_table`).
6. Publishes region/VPC/subnet stats with `ansible.builtin.set_stats`.

## Inputs
- `create_vm_aws_region` (required): Region used across all AWS resources.
- `aws_vpc_name` (default: `aws-test-vpc`)
- `aws_owner_tag` (default: `default`)
- `aws_purpose_tag` (default: `ansible_demo`)
- `aws_tenancy` (default: `default`)
- `aws_vpc_cidr_block` (default: `10.0.0.0/16`)
- `aws_subnet_cidr` (default: `10.0.1.0/24`)
- `aws_sg_name` (default: `aws-test-sg`)
- `aws_subnet_name` (default: `aws-test-subnet`)
- `aws_rt_name` (default: `aws-test-rt`)
- `_azs` (defined in playbook): Region-to-AZ map used to pick subnet AZ.

## Outputs
- `stat_aws_region`
- `stat_aws_vpc_id`
- `stat_aws_vpc_cidr`
- `stat_aws_subnet_id`
- `stat_aws_subnet_cidr`

## Side Effects / Notes
- Creates AWS network resources (VPC, IGW, SG, subnet, route table).
- Security group opens multiple ports publicly and within VPC CIDR; validate against security requirements before production use.

# Containerlab on AWS

Deploy virtual network devices (Cisco Nexus 9000v, Catalyst 8000v) using
[containerlab](https://containerlab.dev/) on a KVM-capable EC2 instance with
nested virtualization.

## Prerequisites

- AWS credentials configured for Ansible (`amazon.aws` collection)
- Access to the container image registry
  (`registry.gitlab.com/redhatautomation/`)
- An SSH keypair will be created automatically

## Two-Step Deployment

### Step 1 — Provision the hypervisor

```bash
ansible-playbook containerlab/provision_hypervisor.yml \
  -e clab_aws_region=us-east-2
```

Creates a VPC, security group, keypair, and launches a `c8i.2xlarge` EC2
instance with nested virtualization enabled plus a 100 GiB EBS volume for
container image storage.

### Step 2 — Deploy containerlab

```bash
ansible-playbook containerlab/deploy_containerlab.yml \
  -e clab_host_ip=<ip-from-step-1> \
  -e clab_aws_keypair_name=clab-key
```

Installs podman, syncs the virtual router images, installs containerlab, and
deploys the `product_demos` topology.

## Connecting to devices

Devices are exposed via port-mapped SSH through the EC2 host:

| Device | Port | Credentials        |
|--------|------|--------------------|
| n9kv   | 2122 | `admin / admin@123` |
| cat8kv | 2123 | `admin / admin@123` |

```bash
ssh -p 2122 admin@<ec2-public-ip>   # Nexus 9000v
ssh -p 2123 admin@<ec2-public-ip>   # Catalyst 8000v
```

## Teardown

```bash
# Destroy the containerlab topology only (keep the EC2 instance)
ansible-playbook containerlab/teardown_containerlab.yml \
  -e clab_host_ip=<ip> -e clab_aws_keypair_name=clab-key

# Destroy everything (EC2, VPC, keypair)
ansible-playbook containerlab/teardown_hypervisor.yml \
  -e clab_aws_region=us-east-2
```

## Instance sizing

| Instance      | vCPU | RAM    | Use case                          |
|---------------|------|--------|-----------------------------------|
| `c8i.2xlarge` | 8    | 16 GiB | Default — n9kv-lite + cat8kv      |
| `c8i.4xlarge` | 16   | 32 GiB | Full-size images / larger topologies |

## Regions

Only `us-east-2` and `us-west-2` are supported. `us-east-1` is explicitly
excluded.

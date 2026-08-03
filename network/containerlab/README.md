# Containerlab on AWS

Deploy virtual network devices (Cisco Nexus 9000v, Catalyst 8000v) using
[containerlab](https://containerlab.dev/) on a KVM-capable EC2 instance with
nested virtualization.

<<<<<<< HEAD
## Deploying from AAP

The recommended way to use this feature is through Ansible Automation Platform.
Run the **APD | Single demo setup** job template with `demo: network` to
configure all job templates and workflows listed below.

### Workflows

| Workflow | Description |
|----------|-------------|
| **NETWORK \| Deploy Containerlab Stack** | Provisions the hypervisor then deploys the topology end-to-end |
| **NETWORK \| Destroy Containerlab Stack** | Tears down the topology then destroys all AWS resources |

Both workflows prompt for **AWS Region** (`us-east-2` or `us-west-2`) and
**Instance Type** (`c8i.2xlarge` or `c8i.4xlarge`) via survey.

### Job Templates

| Job Template | Description |
|---|---|
| **NETWORK \| Containerlab \| Provision Hypervisor** | Creates VPC, security group, keypair, and EC2 instance with nested virtualization |
| **NETWORK \| Containerlab \| Deploy Topology** | Installs podman + containerlab, syncs images, deploys the topology |
| **NETWORK \| Containerlab \| Configure Devices** | Applies NTP, SNMP, and banner configuration to the n9kv and cat8kv |
| **NETWORK \| Containerlab \| Teardown Topology** | Destroys the containerlab topology (keeps the EC2 instance) |
| **NETWORK \| Containerlab \| Teardown Hypervisor** | Terminates the EC2 instance and deletes all VPC resources |

### Credentials

The **Containerlab SSH** Machine credential is created by the setup and
populated automatically by the provision playbook with the EC2 keypair. It is
used by the deploy and teardown templates to SSH into the hypervisor.

## Deploying from the CLI

If you are not using AAP, the playbooks can be run directly with
`ansible-playbook`. AWS credentials must be set via environment variables or
`~/.aws/credentials`.

```bash
# Step 1 — Provision the hypervisor
ansible-playbook network/containerlab/provision_hypervisor.yml \
  -e clab_aws_region=us-east-2

# Step 2 — Deploy containerlab (use the IP from step 1 output)
ansible-playbook network/containerlab/deploy_containerlab.yml \
  -e clab_host_ip=<ip-from-step-1> \
  -e clab_aws_keypair_name=clab-key

# Configure the devices
ansible-playbook network/containerlab/configure_devices.yml \
  -e clab_aws_region=us-east-2

# Teardown
ansible-playbook network/containerlab/teardown_containerlab.yml \
  -e clab_host_ip=<ip> -e clab_aws_keypair_name=clab-key
ansible-playbook network/containerlab/teardown_hypervisor.yml \
  -e clab_aws_region=us-east-2
```

=======
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

>>>>>>> 4a3258b (feat: add containerlab network demo with AWS nested virtualization)
## Connecting to devices

Devices are exposed via port-mapped SSH through the EC2 host:

<<<<<<< HEAD
| Device | Port | Network OS | Credentials |
|--------|------|------------|-------------|
| n9kv   | 2122 | `cisco.nxos.nxos` | `admin / admin@123` |
| cat8kv | 2123 | `cisco.ios.ios` | `admin / admin@123` |
=======
| Device | Port | Credentials        |
|--------|------|--------------------|
| n9kv   | 2122 | `admin / admin@123` |
| cat8kv | 2123 | `admin / admin@123` |
>>>>>>> 4a3258b (feat: add containerlab network demo with AWS nested virtualization)

```bash
ssh -p 2122 admin@<ec2-public-ip>   # Nexus 9000v
ssh -p 2123 admin@<ec2-public-ip>   # Catalyst 8000v
```

<<<<<<< HEAD
## Instance sizing

| Instance | vCPU | RAM | Use case |
|----------|------|-----|----------|
| `c8i.2xlarge` | 8 | 16 GiB | Default — n9kv-lite + cat8kv |
| `c8i.4xlarge` | 16 | 32 GiB | Full-size images / larger topologies |
=======
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
>>>>>>> 4a3258b (feat: add containerlab network demo with AWS nested virtualization)

## Regions

Only `us-east-2` and `us-west-2` are supported. `us-east-1` is explicitly
excluded.

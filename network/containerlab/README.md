# Containerlab on AWS

Deploy virtual network devices (Cisco Nexus 9000v, Catalyst 8000v) using
[containerlab](https://containerlab.dev/) on a KVM-capable EC2 instance with
nested virtualization.

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

## Connecting to devices

Devices are exposed via port-mapped SSH through the EC2 host:

| Device | Port | Network OS | Credentials |
|--------|------|------------|-------------|
| n9kv   | 2122 | `cisco.nxos.nxos` | `admin / admin@123` |
| cat8kv | 2123 | `cisco.ios.ios` | `admin / admin@123` |

```bash
ssh -p 2122 admin@<ec2-public-ip>   # Nexus 9000v
ssh -p 2123 admin@<ec2-public-ip>   # Catalyst 8000v
```

## Instance sizing

| Instance | vCPU | RAM | Use case |
|----------|------|-----|----------|
| `c8i.2xlarge` | 8 | 16 GiB | Default — n9kv-lite + cat8kv |
| `c8i.4xlarge` | 16 | 32 GiB | Full-size images / larger topologies |

## Regions

Only `us-east-2` and `us-west-2` are supported. `us-east-1` is explicitly
excluded.

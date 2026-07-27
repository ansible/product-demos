# Feature
We're going to add a Containerlab component to this project and for our demo-platform (RHDP) catalog item (CI). This involves a two step deployment process. Firstly it will use the AWS crednetials to deploy a hypervisor using an ansible playbook. Once the machine is provisioned, it will install containerlab and deploy some baseline images (such as those used in `../mad-hatter/roles/clab/`). Next, we will build device definitions and bring them up via containerlab and wait for them to be ready. Once they're up and avilable we will build ansible playbooks to connect to them. Note that the network connections must be considered as our testing takes place from outside AWS. For now we must find a simple way to connect to the hosts (likely through a jump-host pattern). 


Later versions of this wil leverage automation content (job templates defined as Config as code) which use the `infra.aap_configuration.dispatch` to configure an AAP instance with this automation content. This is the `setup` portion of this feature.  The user then has access to run this two step process by kicking off the `setup` to provision infrastructure and then launch the jobe template. For now, we'll just use ansible playbooks and move to config as code later.


## Challenges
A major motivation is cost. We want to be able to demontrate the functionality of automating network devices but without having to pay the high cost of full-featured metal instances on AWS. 

Originally the motivation was to use the `a1.metal` instances (graviton). However, I want to investigate using nested virtualization on x86_64 (e.g. using `c8i.xlarge` which is even more inexpensive than `a1.metal`).  Of note, we whould never use `us-east-1`, we will give the user the ability to deploy in `us-east-2` or `us-west-2`. We may also need to add a large disk to the VM in order to sync the images we are using.

## Design

### Instance Type
- Default `c8i.2xlarge` (8 vCPU, 16 GiB) with nested virtualization enabled via `cpu_options`.
- Survey option for `c8i.4xlarge` (16 vCPU, 32 GiB) for larger topologies.
- ARM/`a1.metal` ruled out: vrnetlab images are x86_64 QEMU VMs; ARM would need software emulation.

### Topology
- Start with `product_demos` (n9kv + cat8kv) adapted from `../mad-hatter/roles/clab/`.
- Port-mapped SSH: host ports 2122/2123 map to container port 22.

### Playbooks
- `containerlab/provision_hypervisor.yml` — VPC, SG, keypair, EC2 w/ nested virt, 100 GiB EBS.
- `containerlab/deploy_containerlab.yml` — podman, images, clab install, topology deploy, wait-for-ready.
- `containerlab/teardown_containerlab.yml` — destroy topology only.
- `containerlab/teardown_hypervisor.yml` — destroy all AWS resources.
- `containerlab/setup.yml` — AAP Config as Code placeholder (deferred).

### Regions
- `us-east-2` (default) and `us-west-2` only.

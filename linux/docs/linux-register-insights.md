# Register with Insights


Registers RHEL EC2 instances with Red Hat Subscription Manager using an activation key and org ID. Removes RHUI packages, installs subscription-manager, sets the hostname, and registers the host. Required before RHEL advisory patching.

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>
- <strong>RHSM Registration</strong> credential with org ID and activation key

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Register with Insights | [`linux/ec2_register.yml`](https://github.com/ansible/product-demos/blob/main/linux/ec2_register.yml) | Registers RHEL hosts with RHSM, removes RHUI packages, and configures subscription access |

## Related demos

| Demo | Description |
|------|-------------|
| 🩹 [Patch Cloud Stack in AWS](/product-demos/demos/patch-cloud-stack/) | RHSM registration is required for RHEL patching in this workflow |
| 🐧 [Patching](/product-demos/demos/linux-patching/) | Patch hosts after registering them |

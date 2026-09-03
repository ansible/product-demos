# Destroy Containerlab Stack


Tears down everything created by Deploy Containerlab Stack — destroys the running containerlab topology, then deletes the EC2 hypervisor and related AWS resources (VPC, subnet, security group, keypair). Topology teardown is best-effort so hypervisor cleanup still runs if the instance is already gone.

## Prerequisites

- A stack previously deployed with **NETWORK ǀ Deploy Containerlab Stack**
- AWS credential configured

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| AWS Region | `clab_aws_region` | multiplechoice | Yes |

Options: `us-east-2`, `us-west-2` — use the same region as Deploy.

## Workflow

```mermaid
graph LR
  S["🏠 Start"]
  S --> A
  A["📦 Teardown Topology"] -->|always| B["💥 Teardown Hypervisor"]
  style S fill:#212427,stroke:#8a8d90,color:#fff
```

1. **Teardown Topology** — Runs `containerlab destroy` on the hypervisor when SSH is reachable; skips cleanly if the host is unreachable or not found
2. **Teardown Hypervisor** — Always runs next: terminates the EC2 instance and removes VPC, subnet, security group, and keypair

If the hypervisor SSH key is lost or the instance is hung, run **NETWORK ǀ Containerlab ǀ Teardown Hypervisor** directly or use the **Destroy Containerlab Stack** workflow, which always proceeds to AWS cleanup.

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ Destroy Containerlab Stack | [`network/setup.yml`](../setup.yml) | Workflow that tears down topology then AWS resources |
| NETWORK ǀ Containerlab ǀ Teardown Topology | [`network/teardown_containerlab.yml`](../teardown_containerlab.yml) | Destroys the running containerlab topology |
| NETWORK ǀ Containerlab ǀ Teardown Hypervisor | [`network/teardown_hypervisor.yml`](../teardown_hypervisor.yml) | Deletes the EC2 hypervisor and related AWS resources |

## Presenter walkthrough

1. **When to use:** End of a demo session or when you need a clean rebuild. Safe to run if topology teardown is a no-op.
2. **Launch:** Select the same AWS region used for Deploy.
3. **Watch always_nodes:** Topology teardown feeds hypervisor teardown on the `always` path so AWS cleanup is not skipped.

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Containerlab Stack](./network-deploy-containerlab-stack.md) | The matching provisioning workflow |

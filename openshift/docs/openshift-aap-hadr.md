# AAP HA/DR on OpenShift

Validate an active/passive Ansible Automation Platform deployment across two
OpenShift clusters before introducing controlled switchover or emergency
failover operations.

The implementation follows the [AAP HA/DR on OpenShift solution guide](https://ansible-tmm.github.io/solution-guides/README-AAP-HA-DR-OpenShift)
and targets AAP 2.7. Use the AAP 2.7 Product Demos execution environment for
these jobs:

```text
quay.io/ansible-product-demos/apd-ee-27:latest
```

## Prerequisites

- Two OpenShift 4.14+ clusters in separate failure domains
- Active `KUBECONFIG` with contexts for both clusters
- An `aap` namespace on both clusters
- AAP Operator, CloudNativePG, and External Secrets Operator installed
- AAP and CNPG custom resources deployed on both clusters
- Cross-cluster database replication and replicated object storage configured

## Job templates

| Job template | Purpose | Mutates the cluster |
| --- | --- | --- |
| **OpenShift ǀ AAP HA/DR ǀ Preflight** | Checks cluster versions, namespace, operators, AAP resources, and CNPG resources. | No |
| **OpenShift ǀ AAP HA/DR ǀ Verify** | Confirms the expected active/passive `idle_aap` state and reports platform/database resources. | No |

## Current limitation

Switchover, emergency failover, and failback are deliberately not exposed as
APD jobs yet. A safe implementation must coordinate CNPG promotion, AAP
`idle_aap`, DNS/GSLB, and GitOps reconciliation together. It also requires a
separate confirmation and credential model for destructive operations.

## Validation sequence

1. Run **Preflight** against both cluster contexts.
2. Confirm CNPG replication and object-storage replication independently.
3. Run **Verify** and confirm that the primary has `idle_aap: false` and the
   standby has `idle_aap: true`.
4. Validate AAP access through the stable vanity URL.
5. Record the measured RTO/RPO before implementing the mutation workflows.

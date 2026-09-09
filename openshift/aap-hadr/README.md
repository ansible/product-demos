# AAP HA/DR on OpenShift

This demo provides a product-demo integration point for the active/passive AAP
HA/DR architecture described in the [AAP HA/DR on OpenShift implementation
guide](https://ansible-tmm.github.io/solution-guides/README-AAP-HA-DR-OpenShift).

The initial implementation is intentionally read-only. It validates two
OpenShift sites, CloudNativePG replication, AAP health, and the expected
`idle_aap` state before any switchover or failover automation is enabled.

## Scope

The platform team must provide the underlying infrastructure:

- Two OpenShift 4.14+ clusters in separate failure domains
- AAP 2.7 Operator, CloudNativePG, and External Secrets Operator
- Three-node CNPG clusters with cross-site WAL replication
- Replicated S3-compatible storage for WAL, backups, and Automation Hub content
- Shared AAP encryption keys and database credentials
- A stable vanity URL and DNS/GSLB cutover capability

The playbooks in this directory use the active `KUBECONFIG` and named
OpenShift contexts. They do not contain credentials or secret material.

## Variables

Start from [`vars/example.yml`](vars/example.yml). The two context names and
the AAP namespace are the minimum required inputs.

## Usage

Run the preflight before deploying or changing either site:

```bash
ansible-navigator run openshift/aap-hadr/preflight.yml -m stdout \
  -e @openshift/aap-hadr/vars/example.yml \
  --eei quay.io/ansible-product-demos/apd-ee-27:latest
```

Run health verification after the platform is deployed:

```bash
ansible-navigator run openshift/aap-hadr/verify.yml -m stdout \
  -e @openshift/aap-hadr/vars/example.yml \
  --eei quay.io/ansible-product-demos/apd-ee-27:latest
```

Planned switchover, emergency failover, and failback are not enabled by this
initial slice. Those operations must coordinate CNPG promotion, AAP
`idle_aap`, DNS/GSLB, and any GitOps reconciler as one transaction.

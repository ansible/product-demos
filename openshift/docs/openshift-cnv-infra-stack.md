# CNV — Infra Stack


Deploys the full OpenShift CNV infrastructure stack -- installs the OpenShift Virtualization operator, configures cluster settings, provisions RHEL VMs, and syncs the CNV inventory. The OpenShift equivalent of Deploy Cloud Stack in AWS.

## Workflow

```
Deploy RHEL8 VM ──┐
                  ├──→ Update Inventory
Deploy RHEL9 VM ──┘
    (failure) ──→ Ticket - Instance Failed
```

1. **Deploy VMs** (parallel) — Provisions RHEL 8 and RHEL 9 VMs on CNV
2. **Update Inventory** — Syncs the CNV dynamic inventory so new VMs appear in AAP
3. **Ticket** (on failure) — Creates a notification if VM deployment fails

## Prerequisites

- <strong>OpenShift Credential</strong> configured with API token
- Cluster admin access with bare-metal or nested-virt nodes
- Run <strong>APD | Single demo setup</strong> with <code>openshift</code>

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ CNV ǀ Infra Stack (workflow) | [`openshift/setup.yml`](https://github.com/ansible/product-demos/blob/main/openshift/setup.yml) | Installs CNV, provisions VMs, and syncs inventory in a single workflow |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Create RHEL VM](/product-demos/demos/openshift-cnv-create-vm/) | Create additional VMs after the stack is deployed |
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | The AWS equivalent of this infrastructure workflow |

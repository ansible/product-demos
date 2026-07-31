# CNV — Patch Workflow


Patching workflow for RHEL VMs running on OpenShift Virtualization. Similar to the cloud patching workflow but targeting CNV-managed virtual machines instead of EC2 instances.

## Workflow

```
Take Snapshot ──→ Project Sync  ──┐
              ├──→ Inventory Sync ┴──→ Patch Instance
                                        ├─ (success) done
                                        └─ (failure) Restore from Snapshot
                                                       └─ (failure) Ticket - Restore Failed
```

1. **Take Snapshot** — Creates VM snapshots for recovery
2. **Project Sync + Inventory Sync** (parallel) — Refreshes project content and CNV inventory
3. **Patch Instance** — Applies patches to CNV RHEL VMs
4. **Restore** (on failure) — Restores VMs from snapshot if patching fails
5. **Ticket** (on restore failure) — Creates a notification if restore also fails

## Prerequisites

- RHEL VMs provisioned on OpenShift CNV
- **OpenShift Credential** configured
- SSH connectivity to the CNV VMs

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ CNV ǀ Patch Workflow | [`openshift/setup.yml`](../setup.yml) | Runs the patching workflow against CNV-managed RHEL virtual machines |

## Related demos

| Demo | Description |
|------|-------------|
| 🩹 [Patch Cloud Stack in AWS](../../cloud/docs/patch-cloud-stack.md) | The AWS version of this patching workflow |
| ⎈ [CNV — Infra Stack](./openshift-cnv-infra-stack.md) | Deploy the CNV infrastructure to patch |

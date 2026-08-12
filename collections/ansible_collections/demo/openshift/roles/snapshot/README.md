# demo.openshift.snapshot

Create and restore OpenShift Virtualization (KubeVirt) VM snapshots for hosts selected from inventory.

Set `snapshot_operation` to `create` or `restore` before including the role -- that value selects which task file runs for each VM.

```yaml
- name: Snapshot CNV VMs
  ansible.builtin.include_role:
    name: demo.openshift.snapshot
  vars:
    snapshot_operation: create
    snapshot_hosts: "{{ _hosts }}"
    vm_namespace: openshift-cnv
```

Inventory hostnames are expected in the APD CNV form `<namespace>-<vm name>` (for example `openshift-cnv-rhel9`). The role strips the `vm_namespace-` prefix before calling the KubeVirt APIs. On create, the VM is stopped if running, a `VirtualMachineSnapshot` is taken, then the VM is restarted if it was previously running; the snapshot name is exported with `ansible.builtin.set_stats` for AAP job artifacts. On restore, the latest snapshot for each VM is applied via `VirtualMachineRestore`.

Repo playbook: [`openshift/cnv/snapshot.yml`](../../../../../../openshift/cnv/snapshot.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: OpenShift cluster with OpenShift Virtualization (CNV) installed
- `kubernetes.core` and `redhat.openshift_virtualization` collections
- An attached "OpenShift Credential" (type `OpenShift or Kubernetes API Bearer Token`) so `K8S_AUTH_HOST` / `K8S_AUTH_API_KEY` / `K8S_AUTH_VERIFY_SSL` are injected
- Inventory that includes the CNV VMs to snapshot (or a host pattern passed as `snapshot_hosts`)

## Role Variables

This role has no `defaults/main.yml`; callers must supply the variables below.

| Variable | Default | Description |
| --- | --- | --- |
| `snapshot_operation` | required | `create` or `restore` -- selects `tasks/create.yml` or `tasks/restore.yml` |
| `snapshot_hosts` | required | Ansible host pattern (or inventory group expression) of VMs to act on; typically the survey `_hosts` value |
| `vm_namespace` | required | OpenShift namespace that owns the VirtualMachine objects |

## Entry points

The role always runs `tasks/main.yml`, which includes one of the files below based on `snapshot_operation`:

| Entry point | Description |
| --- | --- |
| `create` | Stop each VM if running, create a `VirtualMachineSnapshot`, restart if needed, and export `restore_snapshot_name` via `set_stats`. |
| `restore` | Stop each VM if running, restore from the latest matching `VirtualMachineSnapshot`, and restart if needed. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.openshift`](../../README.md) for the OpenShift CNV patch / snapshot workflow demos in this repository.

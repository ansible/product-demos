# kubevirt
This repo contains an Ansible role that provision one more VMs onto kubevirt/OpenShift Container-native Virtualization (CNV) environment.

Requirements
------------

You need to have the following packages installed on your control machine:

- mkisofs
- genisoimage

Role Variables
--------------

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - name: provision a new vm
      hosts: all
      gather_facts: False
      connection: local
      become: no
      vars:
        target_namespace: openshift-cnv
        template_namespace: openshift-cnv
        pvc_storage_class: hostpath-provisioner
        kubevirt_upload_proxy_url: https://localhost:443
        nodes:
          - name: rhel81test1
            role: rhel
            app_name: kubevirt_test
            memory: 4096
            cpu: 2
            template: rhel81-x64-v1   # there should be a DV with this name on kubernetes/OpenShift environment

License
-------

MIT

Author Information
------------------

Orcun Atakan

## Versioned template images and lifecycle

The node YAML contract is unchanged: set `template` to the stable template name.
The role resolves `<template>-template-disk0` as a CDI DataSource when present,
then selects its current PVC. Legacy templates with a fixed-name DataVolume/PVC
continue to work. The role rejects missing, terminating, unbound, or incomplete
source images before creating a VM and requires its cloned DataVolume to reach
`Succeeded` before reporting deployment readiness.

EFI and guest OS metadata are inherited from the actual source template. Explicit
node `efi` settings take precedence; BIOS templates do not acquire an EFI
bootloader. Windows specialization selects the correct EFI OS partition.

Current VMs use `runStrategy` instead of `running`. Disk placement respects
WaitForFirstConsumer: the VM is started before waiting for its clone. The default
pod network uses masquerade; explicit Multus interfaces retain bridge binding.
An empty `kubevirt_eviction_strategy` inherits cluster policy. The default
`kubevirt_shutdown_grace_period` is 120 seconds; nodes can override it with
`shutdown_grace_period` and can override eviction with `eviction_strategy`.

Linux `user_name` accounts are kept unlocked and receive a valid sudo rule.
`user_password` overrides the supplied Ansible password; `root_password` retains
its existing behavior. A blank Ansible password does not replace an existing
image password. Debian uses SSH port 22 by default.

For cross-namespace cloning, the role creates a source-namespace Role granting
only `create` on `datavolumes/source`, with a distinct binding for each destination
namespace's default service account. Set `kubevirt_clone_manage_role: false` to
use a separately managed `kubevirt_clone_cluster_role_name` instead. The existing
`kubevirt_clone_cluster_role_enable` switch still controls role/binding setup.

`role_action: deprovision` consumes the same explicit `nodes` YAML as provision,
including localhost and AAP runs without a guest inventory. When guest inventory
VM labels are present, it preserves the current play/inventory limit and deletes
only matching nodes. With
`kubevirt_deprov_wait_vm: true`, it waits for VM/VMI, root DV/PVC, remote Service,
and unattend ConfigMap garbage collection. It never removes PVC finalizers.

### Deletion precondition input

For guarded deletion, `kubevirt_expected_vm_preconditions` accepts the legacy
mapping form. When an automation controller may reinterpret numeric-looking
strings in nested extra vars, pass the same data as one JSON string through
`kubevirt_expected_vm_preconditions_json` and omit the legacy mapping. For example:

```yaml
kubevirt_expected_vm_preconditions_json: >-
  {"example-vm":{"uid":"00000000-0000-4000-8000-000000000001","resourceVersion":"000424242"}}
```

The JSON object must name exactly the selected VMs, with each entry containing
only a UUID `uid` and a nonempty, trimmed string `resourceVersion`. The role
passes those decoded strings unchanged as the Kubernetes delete preconditions;
it does not coerce resource versions. If both forms are supplied, they must agree
exactly. Invalid JSON, mismatched names, malformed identifiers, or non-string
resource versions fail before deletion. Omitting both inputs retains the existing
empty-default behavior.

The coordinated builder changes and reproducible three-OS lifecycle tests are
in `hl-build-os-templates`, under `tests/kubevirt`. Install this updated consumer
before using its versioned-image builder; an older installed role still selects
legacy fixed-name disks.

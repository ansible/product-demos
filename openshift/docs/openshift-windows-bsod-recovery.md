# Windows — BSOD Recovery

Automated Blue Screen of Death recovery for Windows Server VMs running on OpenShift Virtualization. Inspired by the [2024 CrowdStrike incident](https://en.wikipedia.org/wiki/2024_CrowdStrike_incident), this demo shows how Ansible Automation Platform can recover Windows systems from critical boot failures at scale using a custom WinPE recovery environment.

## Prerequisites

- OpenShift cluster with **CNV operator installed** (run **OpenShift | CNV | Install Operator** first)
- A **Windows Server OS image** populated in OpenShift Virtualization (e.g. `windows-2022-standard` template)
- **OpenShift Credential** configured with API bearer token
- **APD Machine Credential** configured with Windows administrator credentials
- OCS/ODF storage class available (`ocs-external-storagecluster-ceph-rbd`)

## Workflows

This demo includes three workflows:

### BSOD Recovery (main demo)

The primary workflow that provisions Windows VMs, triggers a simulated BSOD, recovers via WinPE, and verifies the fix.

```
Provision Infrastructure ──→ Inventory Sync ──→ Produce BSOD
                                                    │
                                              Recover from BSOD
                                                    │
                                              Inventory Sync 2
                                                    │
                                              Check System
```

1. **Provision Infrastructure** — Deploys Windows Server VMs on OpenShift Virtualization
2. **Inventory Sync** — Refreshes the CNV dynamic inventory to discover the new VMs
3. **Produce BSOD** — Triggers a simulated Blue Screen of Death on the Windows VMs
4. **Recover from BSOD** — Boots the affected VM into a custom WinPE environment and applies the recovery fix
5. **Inventory Sync 2** — Re-syncs inventory after the VM reboots with the fix applied
6. **Check System** — Verifies the Windows system is healthy and operational

### Generate WinPE Image (prerequisite)

Run this workflow first to build the WinPE recovery ISO that the BSOD Recovery workflow uses.

```
Provision Infrastructure ──→ Inventory Sync ──→ Generate WinPE ──→ Upload WinPE ISO ──→ Remove Infrastructure
```

1. **Provision Infrastructure** — Deploys a Windows Server VM to use as a WinPE build host
2. **Inventory Sync** — Discovers the new VM in inventory
3. **Generate WinPE** — Creates a custom WinPE ISO with embedded recovery scripts
4. **Upload WinPE ISO** — Uploads the ISO to OpenShift Virtualization as a PVC
5. **Remove Infrastructure** — Cleans up the build VM (no longer needed)

### Clean up BSOD VMs

Removes all Windows VMs created by the BSOD Recovery workflow.

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ Windows ǀ Provision Infrastructure | `provision_infra_multi.yml` | Provisions Windows Server VMs on OpenShift Virtualization |
| OpenShift ǀ Windows ǀ Remove Infrastructure | `remove_infra_multi.yml` | Removes provisioned Windows VMs |
| OpenShift ǀ Windows ǀ Generate WinPE | `generate_winpe.yml` | Creates a custom WinPE recovery ISO |
| OpenShift ǀ Windows ǀ Upload WinPE ISO | `upload_winpe_iso.yml` | Uploads the WinPE ISO to OpenShift Virtualization |
| OpenShift ǀ Windows ǀ Produce BSOD | `produce_bsod.yml` | Triggers a simulated BSOD on Windows VMs |
| OpenShift ǀ Windows ǀ Recover from BSOD | `execute_winpe_recovery.yml` | Boots into WinPE and applies the recovery fix |
| OpenShift ǀ Windows ǀ Check System | `check_system.yml` | Verifies the system is healthy after recovery |

## How it works

The recovery process uses a **Windows Preinstallation Environment (WinPE)** — a lightweight Windows boot image that can run recovery scripts without needing the OS to be operational. The workflow:

1. **Generates a custom WinPE ISO** with embedded recovery scripts tailored to the specific failure scenario (e.g. removing a faulty driver file like the CrowdStrike `csagent.sys`)
2. **Boots the affected VM from the WinPE ISO** using OpenShift Virtualization's ability to attach ISO images to VMs
3. **Executes the recovery script** inside WinPE, which mounts the Windows partition and applies the fix
4. **Reboots the VM** back to the repaired Windows installation

This approach works because WinPE can access the Windows filesystem even when Windows itself cannot boot — exactly the scenario during a BSOD.

## Why it matters

- Demonstrates **automated disaster recovery** at scale — manually fixing BSOD on thousands of machines is not feasible
- The 2024 CrowdStrike incident affected ~8.5 million Windows devices — this demo shows how AAP could have automated the fix
- Separating WinPE generation from recovery execution means the same framework handles different BSOD root causes
- Shows AAP managing **Windows workloads on OpenShift** — a powerful cross-platform story

## Presenter walkthrough

1. **Set the stage:** Reference the 2024 CrowdStrike incident — a faulty update bricked millions of Windows machines. IT teams had to manually boot each machine into Safe Mode and delete a file. "What if we could automate that?"
2. **Show the WinPE generation:** If not already done, run the Generate WinPE Image workflow. Explain how the recovery logic is embedded in the ISO.
3. **Launch the BSOD Recovery workflow:** Show the audience the Windows VM running normally, then launch the workflow. The "Produce BSOD" step intentionally crashes the VM.
4. **The blue screen:** Show the VM console — it's stuck on a BSOD. "In the real world, this is where someone walks to the data center."
5. **Automated recovery:** Point out the "Recover from BSOD" step — AAP attaches the WinPE ISO, boots from it, runs the fix script, and reboots. No manual intervention.
6. **Verification:** The "Check System" step confirms Windows is back and healthy. "From crash to recovery, fully automated."
7. **Clean up:** Run the cleanup workflow to remove the demo VMs.

## Talking points

- This is a real-world scenario, not a contrived demo — the CrowdStrike incident made headlines worldwide
- The same WinPE-based approach works for any boot-level Windows issue, not just CrowdStrike
- OpenShift Virtualization provides the VM management APIs that make programmatic ISO attachment possible
- AAP workflows handle the orchestration — provisioning, crashing, recovering, verifying — in a single automation

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [CNV — Install Operator](./openshift-cnv-install.md) | Required prerequisite — installs the CNV operator |
| ⎈ [CNV — Infra Stack](./openshift-cnv-infra-stack.md) | Deploy RHEL VMs on CNV (similar infrastructure provisioning pattern) |
| ⎈ [CNV — Patch Workflow](./openshift-cnv-patch-workflow.md) | Patching workflow for CNV VMs with snapshot/restore |

## Credits

Demo created by [Orcun Atakan](https://github.com/oatakan). The source playbooks and roles are included in `openshift/windows-bsod-recovery/`.

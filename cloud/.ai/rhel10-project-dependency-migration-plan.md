# RHEL10 and Cloud Project Dependency Migration Plan

## Objective
Add `rhel10` as a first-class AWS blueprint option while removing runtime dependency on the external projects:
- `Ansible Cloud AWS Demos`
- `Ansible Cloud Content Lab - AWS`

The target end state is that cloud workflows and templates run only from the main project:
- `Ansible Product Demos`

## Current State Summary
- `cloud/blueprints/rhel10.yml` already exists and defines AWS image selection for RHEL10.
- `common/setup.yml` still defines two external `controller_projects` and points several templates to those projects.
- `cloud/setup.yml` also references templates that currently source playbooks from external projects.
- The `Cloud | AWS | Create VM` survey in `common/setup.yml` does not yet include `rhel10`.
- The cloud deployment workflow in `cloud/setup.yml` deploys `rhel8` and `rhel9` nodes, but not `rhel10`.

## Migration Strategy

### 1) Replace external playbook dependencies with local playbooks
Create local playbook entrypoints in this repository (under `cloud/`) for any templates that currently call external project playbooks. Planned local replacements:
- `cloud/create_vm.yml`
- `cloud/delete_inventory_vm.yml`
- `cloud/create_peer_network.yml`
- `cloud/delete_peer_network.yml`
- `cloud/create_transit_network.yml`
- `cloud/delete_transit_network.yml`
- `cloud/create_reports.yml`
- `cloud/cloud_report.yml`

Implementation guidance:
- Prefer thin wrappers that call existing local role logic from `demo.cloud.aws` where available (`tasks_from` patterns already used by snapshot/restore/resize playbooks).
- Reuse existing inventory/controller/reporting mechanics already present in this repo.
- Keep variable names compatible with current surveys/workflows to minimize downstream changes.

### 2) Repoint controller templates to `Ansible Product Demos`
Update template definitions in:
- `common/setup.yml`
- `cloud/setup.yml`

For each cloud template currently referencing external projects:
- Set `project: Ansible Product Demos`
- Update `playbook:` path to the new local playbook path (`cloud/...`)

This includes at least:
- `Cloud | AWS | Create VM`
- `Cloud | AWS | Delete VM`
- `Cloud | AWS | Create Peer Infrastructure`
- `Cloud | AWS | Delete Peer Infrastructure`
- `Cloud | AWS | Create Transit Infrastructure`
- `Cloud | AWS | Delete Transit Infrastructure`
- `Cloud | AWS | VPC Report`
- `Cloud | AWS | Tags Report`

### 3) Remove external project definitions
In `common/setup.yml`, remove the two `controller_projects` entries:
- `Ansible Cloud Content Lab - AWS`
- `Ansible Cloud AWS Demos`

Retain and use only `Ansible Product Demos` for cloud templates and workflows.

### 4) Enable `rhel10` in VM creation survey
In `common/setup.yml` under `Cloud | AWS | Create VM` survey (`vm_blueprint` choices):
- Add `rhel10`

Validation goal:
- Launching the VM template with `vm_blueprint: rhel10` loads `cloud/blueprints/rhel10.yml` values and resolves an AMI via the existing filter.

### 5) Add RHEL10 workflow node
In `cloud/setup.yml` workflow `Deploy Cloud Stack in AWS`:
- Add `Deploy RHEL10 Blueprint` node parallel to RHEL8/RHEL9 nodes.
- Configure extra data:
  - `create_vm_vm_name: aws_rhel10`
  - `vm_blueprint: rhel10`
- Connect success/failure paths consistently with existing blueprint nodes (`Update Inventory` and `Ticket - Instance Failed`).

### 6) Compatibility and safety checks
Before finalizing:
- Ensure all cloud template `playbook` paths exist locally.
- Ensure template survey variables still match local playbook/role expectations.
- Ensure no remaining references to external project names in `common/setup.yml` or `cloud/setup.yml`.
- Ensure workflows still converge correctly on reporting and inventory updates.

## Validation Checklist
- `rg` in repo shows zero references to:
  - `Ansible Cloud AWS Demos`
  - `Ansible Cloud Content Lab - AWS`
- `Cloud | AWS | Create VM` survey includes `rhel10`.
- `Deploy Cloud Stack in AWS` workflow includes a `Deploy RHEL10 Blueprint` node.
- All cloud templates referenced by workflows point to `project: Ansible Product Demos`.
- All referenced playbook files exist in local repo.

## Rollout Notes
- Apply and test in local repository first.
- Run setup/import path used for controller object reconciliation and verify templates/workflows update cleanly.
- Perform a dry run of VM creation with `rhel10` and confirm AMI selection and instance creation.

## Explicit Repository Constraint
All changes are to be made locally in this repository only.
No push to parent or upstream repository is part of this plan.

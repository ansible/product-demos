# snapshot_ec2.yml

## Purpose
Entry-point playbook that delegates EC2 snapshot operations to shared role logic.

## Execution Context
- Runs on hosts provided by `_hosts`.
- `hosts` is set to `{{ _hosts | default(omit) }}`.
- `gather_facts` is disabled.

## Workflow
1. Includes role `demo.cloud.aws`.
2. Executes role task file `snapshot_vm` via `tasks_from`.

## Inputs
- `_hosts`: Inventory target(s) for snapshot operation.
- Any additional variables required by `demo.cloud.aws` task file `snapshot_vm`.

## Outputs
- No direct `set_stats` output in this wrapper playbook.
- Operational results are produced by the included role tasks.

## Side Effects / Notes
- Actual snapshot behavior is implemented in role `demo.cloud.aws` (`tasks_from: snapshot_vm`).
- This playbook is a thin wrapper around role-based logic.

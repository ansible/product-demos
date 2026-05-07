# resize_ec2.yml

## Purpose
Entry-point playbook that delegates EC2 instance resize operations to shared role logic.

## Execution Context
- Runs on hosts provided by `_hosts`.
- `hosts` is set to `{{ _hosts | default(omit) }}`.
- `gather_facts` is disabled.

## Workflow
1. Includes role `demo.cloud.aws`.
2. Executes role task file `resize_ec2` via `tasks_from`.

## Inputs
- `_hosts`: Inventory target(s) that the resize workflow should run against.
- Any additional variables required by `demo.cloud.aws` task file `resize_ec2`.

## Outputs
- No direct `set_stats` output in this wrapper playbook.
- Operational results are produced by the included role tasks.

## Side Effects / Notes
- Actual resize behavior is implemented in role `demo.cloud.aws` (`tasks_from: resize_ec2`).
- This playbook serves as a thin orchestration wrapper.

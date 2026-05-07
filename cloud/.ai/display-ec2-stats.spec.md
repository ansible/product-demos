# display-ec2-stats.yml

## Purpose
Displays previously collected cloud runtime stats for region, key pair, VPC, and subnet values.

## Execution Context
- Runs on `localhost`.
- `gather_facts` is disabled.

## Workflow
1. Iterates over known stat variable names.
2. Prints each value with `ansible.builtin.debug`.

## Inputs
- Expects these variables to exist in the current run context:
  - `stat_aws_region`
  - `stat_aws_key_pair`
  - `stat_aws_vpc_id`
  - `stat_aws_vpc_cidr`
  - `stat_aws_subnet_id`
  - `stat_aws_subnet_cidr`

## Outputs
- No persistent outputs are written.
- Emits debug output to playbook logs/stdout.

## Side Effects / Notes
- Reporting-only playbook; does not create, update, or delete cloud resources.

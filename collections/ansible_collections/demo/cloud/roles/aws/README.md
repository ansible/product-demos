# demo.cloud.aws

Create, resize, snapshot, restore, and destroy AWS EC2 instances and the supporting VPC/subnet/security-group/keypair infrastructure for the cloud demos.

Invoke with `include_role` and `tasks_from` -- this role has no `tasks/main.yml`, so it cannot be called without selecting an entry point.

```yaml
- name: Include create vm role
  ansible.builtin.include_role:
    name: demo.cloud.aws
    tasks_from: create_vm
```

`create_vm` is idempotent: it first looks for an existing instance matching the full tag set (name, blueprint, environment, deployment, owner, purpose) and reuses it if found, otherwise it resolves the subnet/AMI and creates a new instance; either way the public/private IPs are exported via `set_stats`. The other entry points (`resize_ec2`, `snapshot_vm`, `restore_vm`, `destroy_vm`) act on an existing `instance_id` and are typically run with `delegate_to: localhost` against a host already known to AAP.

Repo playbooks: [`cloud/create_vm.yml`](../../../../../../cloud/create_vm.yml), [`cloud/resize_ec2.yml`](../../../../../../cloud/resize_ec2.yml), [`cloud/snapshot_ec2.yml`](../../../../../../cloud/snapshot_ec2.yml), [`cloud/restore_ec2.yml`](../../../../../../cloud/restore_ec2.yml).

`create_infra` and `destroy_vm` are not currently invoked by any repo playbook -- [`cloud/create_vpc.yml`](../../../../../../cloud/create_vpc.yml)/[`cloud/delete_vpc.yml`](../../../../../../cloud/delete_vpc.yml) and [`cloud/delete_vm_by_name.yml`](../../../../../../cloud/delete_vm_by_name.yml) implement equivalent logic with inline `amazon.aws` tasks instead of this role.

## Requirements

- ansible-core >= 2.16.0
- Target: `localhost` (all tasks are AWS API calls, several explicitly `delegate_to: localhost`)
- `amazon.aws` collection (`ec2_instance`, `ec2_instance_info`, `ec2_vpc_*`, `ec2_vol*`, `ec2_snapshot*`, `ec2_key`, `ec2_security_group`, `ec2_ami_info`)
- `infra.controller_configuration` collection (`inventory_source_update`, used by `resize_ec2` to refresh AAP inventory)
- AWS credentials available to the `amazon.aws` modules (for example an AAP AWS credential injecting the usual `AWS_*` environment variables)

## Role Variables

Defaults live in `defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `aws_vpc_name` / `aws_vpc_prefix` | `ansible` / `demo` | Used to derive the VPC, keypair, and security group names in `create_infra` |
| `aws_vpc_cidr_block` / `aws_subnet_cidr` | `10.0.0.0/16` / `10.0.1.0/24` | CIDRs for the VPC and its subnet (`create_infra`) |
| `aws_region` | `us-east-1` | Region for `create_infra` and the `snapshot_vm` / `restore_vm` / `resize_ec2` entry points |
| `aws_keypair_name` / `aws_securitygroup_name` | derived from `aws_vpc_name`/`aws_vpc_prefix` | Names used by `create_infra` |
| `aws_ec2_wait` | `true` | Whether `create_infra` waits for resources to reach their target state |
| `aws_snapshots` | `{}` | Populated by `snapshot_vm` (`set_stats`) and consumed by `restore_vm` to attach the correct snapshot per volume |
| `create_vm_vm_name` | `demo_vm` | `Name` tag / idempotency key for `create_vm` |
| `create_vm_aws_region` | `us-east-1` | Region for `create_vm` |
| `create_vm_aws_instance_size` | `t2.micro` | Instance type for `create_vm` |
| `create_vm_aws_tenancy` | `default` | Tenancy for `create_vm` |
| `create_vm_vm_deployment` / `create_vm_vm_environment` / `create_vm_vm_owner` / `create_vm_vm_purpose` | `default` / `default` / `ansible` / `demo` | Tags used both for idempotency lookups and on the created instance |
| `create_vm_aws_image_filter` | `RHEL-9*HVM-*Hourly*` | AMI name filter for `ec2_ami_info` |
| `create_vm_aws_image_architecture` | `x86_64` | AMI architecture filter |
| `create_vm_aws_userdata_template` | `default` | Template name (`<name>.j2` in `templates/`) rendered as EC2 user-data; defaults to `default` (`templates/default.j2`). Windows blueprints such as `cloud/blueprints/windows_full.yml` override it to `aws_windows_userdata`. The older `cloud/blueprints/windows.yml` sets the legacy unprefixed `aws_userdata_template` instead, which this role's `create_vm` no longer reads |

`instance_id`, `instance_type`, and `tags` are required caller-supplied variables for `resize_ec2` / `snapshot_vm` / `restore_vm` / `destroy_vm` (not set in `defaults/main.yml`).

## Entry points

| Entry point | Description |
| --- | --- |
| `create_vm` | Reuse a matching existing instance by tag, or resolve the subnet/AMI and create a new one; exports IPs via `set_stats`. |
| `create_infra` | Create the demo VPC, Internet Gateway, security group (WinRM/RDP/HTTP/AD ports), subnet, route table, and keypair. |
| `resize_ec2` | Stop, resize (`instance_type`), and restart an instance, then refresh the AAP AWS inventory source. |
| `snapshot_vm` | Snapshot every EBS volume attached to `instance_id` and record the snapshot IDs in `aws_snapshots` via `set_stats`. |
| `restore_vm` | Stop the instance, detach current volumes, and reattach either the recorded `aws_snapshots` entry or the latest matching snapshot, then restart. |
| `destroy_vm` | Terminate the instance identified by `instance_id`. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.cloud`](../../README.md) for the AWS cloud demos in this repository.

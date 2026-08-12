# demo.cloud.retrieve_info

Gather VPC, EC2 instance, and Internet Gateway information across every region in `ec2_regions`, storing each region's data as a per-region fact for later use by `demo.cloud.template`.

```yaml
- name: Load retrieve info role
  ansible.builtin.include_role:
    name: demo.cloud.retrieve_info
```

For each region, the role sets a fact named after the region (dashes replaced with underscores, for example `us_east_1`) containing `vpc_info`, `ec2_instance_info`, and `igw_info`, and appends it to `all_ec2_regions`. It also records the AWS caller identity (`aws_user`) and the local `boto3` version.

Repo playbook: [`cloud/cloud_report.yml`](../../../../../../cloud/cloud_report.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: `localhost` (all AWS lookups are `delegate_to: localhost`)
- `amazon.aws` collection (`ec2_vpc_net_info`, `ec2_instance_info`, `ec2_vpc_igw_info`, `aws_caller_info`)
- `boto3` importable by the Ansible controller's Python interpreter (queried via `pip` check mode and a `pipe` lookup)
- AWS credentials with read access to VPCs, EC2 instances, and Internet Gateways in each configured region

## Role Variables

Defaults live in `defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `ec2_regions` | ~20 regions (`us-east-1`, `us-west-2`, `eu-west-1`, etc.; several regions commented out) | Regions iterated over to build `all_ec2_regions` |
| `filter_tag` | unset | Optional `ec2_instance_info` filter dict, applied per region |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | For each region in `ec2_regions`, gather VPC/EC2/IGW info and store it as a per-region fact; also records `aws_user` and the local `boto3` version. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.cloud`](../../README.md) for the AWS cloud reporting demos in this repository.

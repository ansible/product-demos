# demo.cloud.retrieve_aws_instances_info

Gather package/service facts and OS diagnostics from an EC2 instance, then verify the instance's public webserver (and OpenSCAP reports path) are reachable, for the cloud infrastructure report.

```yaml
- name: Load retrieve info role
  ansible.builtin.include_role:
    name: demo.cloud.retrieve_aws_instances_info
```

Runs against each EC2 instance itself (not `localhost`): it gathers `service_facts`, checks `/etc/motd` and `getenforce`, then delegates to `localhost` to look up the instance's EC2 info by private IP and probe `http://<public_dns>/` and `http://<public_dns>/oscap-reports/`.

Repo playbook: [`cloud/cloud_report.yml`](../../../../../../cloud/cloud_report.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: an EC2 instance reachable by Ansible, with facts gathered (`ansible_default_ipv4.address`)
- `amazon.aws` collection (`ec2_instance_info`)
- AWS credentials available for the `delegate_to: localhost` lookup

## Role Variables

This role has no `defaults/main.yml`; it uses `reports_aws_region` (falling back to `aws_region`, then `us-east-1`) from the caller/other cloud roles.

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Gather service facts, SELinux status, and `/etc/motd` presence; look up the instance's EC2 info by private IP; verify the webserver and `/oscap-reports/` path respond over HTTP. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.cloud`](../../README.md) for the AWS cloud reporting demos in this repository.

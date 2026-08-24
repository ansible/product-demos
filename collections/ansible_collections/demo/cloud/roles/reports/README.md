# demo.cloud.reports

Create an S3-hosted static website bucket, sync a local report directory into it, publish a landing page, and (via the `vpc` entry point) render and upload a VPC infrastructure report.

```yaml
- name: Publish VPC report to S3
  ansible.builtin.include_role:
    name: demo.cloud.reports
```

`tasks/main.yml` always creates/configures the bucket and syncs `files/`, then dynamically includes `{{ reports_aws_report }}.yml` (`vpc` by default) to build the report-specific content before uploading `index.html`.

This role is not currently referenced by any repo playbook or job template. The active `Cloud | AWS | VPC Report` path uses [`cloud/cloud_report.yml`](../../../../../../cloud/cloud_report.yml) with `demo.cloud.retrieve_info` → `demo.cloud.template` → `demo.cloud.build_report_s3` instead. Kept for direct use or future wiring.

## Requirements

- ansible-core >= 2.16.0
- Target: `localhost`
- `amazon.aws` collection (`s3_bucket`, `s3_object`, `s3_object_info`, `ec2_vpc_net_info`, `ec2_instance_info`, `ec2_vpc_igw_info`, `aws_caller_info`)
- `community.aws` collection (`s3_website`, `s3_sync`)
- AWS credentials with permission to create/configure S3 buckets and read VPC/EC2/IGW info

## Role Variables

Defaults live in `defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `reports_aws_region` | `us-east-1` | Region for the S3 bucket and the AWS info lookups used by `vpc.yml` |
| `reports_aws_staging_dir` | `{{ playbook_dir \| default('/tmp') }}` | Local directory where rendered HTML is staged before upload |
| `reports_aws_bucket_prefix` | first 4 chars of `AWS_ACCESS_KEY_ID` (lowercased) | Used to derive a unique bucket name |
| `reports_aws_bucket_name` | `{{ reports_aws_bucket_prefix }}-reports` | S3 bucket created/configured as a static website |
| `reports_aws_bucket_permissions` | `public-read` | ACL/permission applied to uploaded objects |
| `reports_aws_public_access` | all `false` (public) | `public_access` block passed to `s3_bucket` |
| `reports_aws_report` | `vpc` | Report task file (`{{ reports_aws_report }}.yml`) included after the bucket/website is configured |
| `reports_aws_instance_filters` | `{{ omit }}` | Optional filters for EC2 instance info lookups |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Create/configure the report bucket and website, sync `files/`, then include `{{ reports_aws_report }}.yml`, upload the resulting `index.html`, and print the bucket URL. |
| `vpc` | Gather VPC, EC2 instance, and Internet Gateway info for `reports_aws_region`, template `vpc-report.html`, and upload it to the bucket. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.cloud`](../../README.md) for the AWS VPC reporting demos in this repository.

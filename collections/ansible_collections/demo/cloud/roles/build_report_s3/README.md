# demo.cloud.build_report_s3

Create (or update) an S3 bucket configured as a static website, sync a local report directory into it, and publish an `index.html`, for AWS cloud demo reports hosted directly on S3 instead of a VM.

```yaml
- name: Load report to host on AWS S3
  ansible.builtin.include_role:
    name: demo.cloud.build_report_s3
  when: inventory_hostname == 'localhost'
```

Run after `demo.cloud.retrieve_info` and `demo.cloud.template` have rendered `index.html` in `playbook_dir`. The bucket policy is rendered from `templates/policy.json` to allow public read access to the website content.

Repo playbook: [`cloud/cloud_report.yml`](../../../../../../cloud/cloud_report.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: `localhost`
- `amazon.aws` collection (`s3_bucket`, `s3_object`, `s3_object_info`)
- `community.aws` collection (`s3_website`, `s3_sync`)
- AWS credentials with permission to create/configure S3 buckets and objects

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `reports_aws_bucket_name` | `aws-cloud-report` | S3 bucket created/configured as a static website |
| `reports_aws_region` | `us-west-1` | AWS region for the bucket |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Create the report bucket (public-read policy from `templates/policy.json`), enable static website hosting, sync `files/` from `playbook_dir`, upload `index.html`, and print the bucket website URL. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.cloud`](../../README.md) for the AWS cloud reporting demos in this repository.

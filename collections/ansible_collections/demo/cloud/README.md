# demo.cloud

Local collection containing roles used by the [Cloud demos](../../../../cloud/README.md) in ansible-product-demos.

This collection is not published to Ansible Galaxy or Automation Hub; it exists solely to organize roles used by playbooks in this repository under the `demo.cloud` namespace.

## Contents

### Roles

| Role | Description |
|------|-------------|
| [aws](roles/aws/README.md) | Create, resize, snapshot, restore, and destroy AWS EC2 instances and supporting VPC infrastructure. |
| [build_report_s3](roles/build_report_s3/README.md) | Build and publish an HTML report to an S3-hosted static website. |
| [build_report_linux](roles/build_report_linux/README.md) | Install Apache and build an HTML report from Linux services and packages facts. |
| [manage_direct_peered_networks](roles/manage_direct_peered_networks/README.md) | Create or delete a direct VPC peering model (DMZ + private network) in AWS. |
| [manage_transit_peered_networks](roles/manage_transit_peered_networks/README.md) | Create or delete a hub-and-spoke transit gateway VPC network model in AWS. |
| [reports](roles/reports/README.md) | Create an S3-hosted report bucket, sync report files, and publish a landing page. |
| [retrieve_aws_instances_info](roles/retrieve_aws_instances_info/README.md) | Gather service/package facts and verify EC2 instance and webserver reachability. |
| [retrieve_info](roles/retrieve_info/README.md) | Retrieve VPC, EC2 instance, and Internet Gateway information for one or more AWS regions. |
| [template](roles/template/README.md) | Shared report page templates (header, footer, VPC, ansible) used by the reporting roles. |

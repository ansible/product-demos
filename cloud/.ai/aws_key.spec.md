# aws_key.yml

## Purpose
Creates or updates an AWS EC2 key pair for the demo environment and publishes the key pair name as a runtime stat for downstream playbooks.

## Execution Context
- Runs on `localhost`.
- Requires AWS credentials/config to be available to Ansible AWS modules.

## Workflow
1. Validates required input variables are defined.
2. Creates/imports the key pair using `amazon.aws.ec2_key` with provided public key material.
3. Stores `stat_aws_key_pair` using `ansible.builtin.set_stats`.

## Inputs
- `create_vm_aws_region` (required): AWS region where key pair is managed.
- `aws_public_key` (required): Public key contents to import.
- `aws_key_name` (default: `aws-test-key`): Key pair name.
- `aws_keypair_owner` (required in assertions): Value used for `owner` tag.

## Outputs
- `stat_aws_key_pair`: Key pair name for later playbook consumption.

## Side Effects / Notes
- Creates or updates an EC2 key pair in AWS.
- Applies an `owner` tag to the key pair.

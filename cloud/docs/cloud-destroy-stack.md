---
layout: demo-detail
demo_slug: cloud-destroy-stack
---
# Destroy Cloud Stack in AWS


Tears down everything created by Deploy Cloud Stack in AWS — terminates all five stack VMs in parallel, deletes the VPC and related networking resources, deletes the keypair, and re-syncs the AWS dynamic inventory so hosts are removed from AAP.

## Prerequisites

- A stack previously deployed with <strong>Deploy Cloud Stack in AWS</strong>
- AWS credential configured

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| AWS Region | `aws_region` | multiplechoice | Yes |

## Presenter walkthrough

1. <strong>When to use:</strong> Run this at the end of a demo session or when you need to start fresh. It's safe to run even if some VMs are already terminated.
2. <strong>Launch:</strong> Select the same AWS region used for Deploy. The workflow handles everything else.
3. <strong>Watch the parallel teardown:</strong> All five VMs are terminated simultaneously, then VPC and keypair cleanup happens.

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | The matching provisioning workflow |

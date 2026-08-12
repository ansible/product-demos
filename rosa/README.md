# ROSA (Red Hat OpenShift on AWS) Lifecycle Demo

Demonstrates automated ROSA cluster lifecycle management through Ansible Automation Platform: preflight validation, creation, readiness verification, and safe destruction.

## Workflows

| Workflow | Description |
|----------|-------------|
| ROSA ǀ Lifecycle (Create) | End-to-end cluster creation with preflight checks and failure-safe destroy |
| ROSA ǀ Lifecycle (Destroy) | Safe cluster teardown with orphaned resource cleanup |

## Job Templates

| Job Template | Description |
|--------------|-------------|
| ROSA ǀ Preflight Checks | Validates credentials, permissions, quotas, and name conflicts |
| ROSA ǀ Create Cluster | Initiates STS-mode ROSA cluster creation |
| ROSA ǀ Wait for Ready | Polls until cluster is ready, creates admin credentials |
| ROSA ǀ Destroy Cluster | Removes cluster, operator roles, and OIDC provider |

## Prerequisites

1. **ROSA Lifecycle EE** — built and pushed to `quay.io/acme_corp/rosa-ee:latest`
2. **AWS Credential** — IAM user/role with ROSA permissions (see docs)
3. **ROSA Token Credential** — API token from [console.redhat.com](https://console.redhat.com/openshift/token/rosa)
4. **AWS service quotas** — sufficient EC2, VPC, ELB limits in target region

## Cost Warning

ROSA clusters incur significant AWS charges (~$0.171/hr control plane + compute costs). Always destroy clusters after demos. Use the TTL tag for tracking.

## Documentation

- [Operator Runbook & Troubleshooting](docs/rosa-lifecycle.md)

# ROSA — Cluster Lifecycle

Automated Red Hat OpenShift Service on AWS (ROSA) cluster lifecycle management: preflight validation, creation, readiness verification, and safe destruction — all orchestrated through AAP workflows.

## Prerequisites

- AWS credential configured with [ROSA STS required IAM permissions](https://docs.openshift.com/rosa/rosa_planning/rosa-sts-aws-prereqs.html)
- ROSA Token credential (obtain offline token from https://console.redhat.com/openshift/token/rosa)
- ROSA Lifecycle EE available (`quay.io/acme_corp/rosa-ee:latest`)
- Sufficient AWS service quotas (EC2, VPC, ELB, EIP) in target region

## Configure credentials

| Credential | Type | Where to get it |
|------------|------|-----------------|
| AWS | Amazon Web Services | IAM console — Access Key + Secret |
| ROSA Token | ROSA Token (custom) | https://console.redhat.com/openshift/token/rosa → "use API tokens" → Load token |

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Cluster Name | `rosa_cluster_name` | text | Yes |
| AWS Region | `rosa_aws_region` | multiplechoice | Yes |
| Compute Nodes | `rosa_compute_nodes` | multiplechoice | Yes |
| Machine Type | `rosa_compute_machine_type` | multiplechoice | Yes |
| OpenShift Version | `rosa_version` | text | No |
| Cluster TTL | `rosa_ttl` | text | Yes |
| Owner Tag | `rosa_owner_tag` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| ROSA ǀ Preflight Checks | [`rosa/preflight.yml`](../preflight.yml) | Validates credentials, permissions, quotas, EIP availability, and name conflicts |
| ROSA ǀ Create Cluster | [`rosa/create.yml`](../create.yml) | Creates account roles, ensures EIP quota, and initiates STS-mode cluster creation |
| ROSA ǀ Wait for Ready | [`rosa/wait.yml`](../wait.yml) | Polls cluster status until ready, creates cluster-admin credentials |
| ROSA ǀ Destroy Cluster | [`rosa/destroy.yml`](../destroy.yml) | Tears down cluster, operator roles, and OIDC provider (idempotent) |

## Why it matters

ROSA cluster provisioning involves multiple AWS services, IAM role chains, and a 30-40 minute wait. Manual creation is error-prone and forgetting teardown leads to significant cost. This demo shows how AAP:

- **Gates creation** with deterministic preflight checks (fail fast, not 30 minutes in)
- **Automates AWS prerequisites** (account roles, EIP quota management)
- **Provides self-service** via surveys with guardrails (naming conventions, TTL tags)
- **Ensures cleanup** via destroy-on-failure workflow paths
- **Reduces cost risk** with idempotent destruction and orphaned resource guidance

## Presenter walkthrough

1. Show the **ROSA ǀ Lifecycle (Create)** workflow visualization — highlight the destroy-on-failure safety path
2. Launch the workflow; while waiting (~35 min), discuss the preflight output and what it validated
3. Show the cluster in the [Red Hat OpenShift console](https://console.redhat.com/openshift) once ready
4. Log in using the cluster-admin credentials from the Wait job output
5. Demonstrate **ROSA ǀ Lifecycle (Destroy)** to show clean teardown

## Talking points

- ROSA is a jointly-managed service: Red Hat manages the control plane, AWS provides the infrastructure
- STS mode means no long-lived credentials are stored in the cluster
- AAP handles the multi-step orchestration that would otherwise require a runbook
- Tagging strategy enables cost attribution and automated cleanup audits
- The same pattern works for any managed Kubernetes service (EKS, ARO, GKE)

## Expected timings

| Phase | Duration |
|-------|----------|
| Preflight | 1-2 min |
| Create (initiate) | 2-3 min |
| Wait for ready | 30-40 min |
| Destroy | 15-25 min |

## Cost warning

ROSA clusters cost ~$0.55/hour (control plane + 2× m5.xlarge). Always destroy after demos.

## Related demos

| Demo | Description |
|------|-------------|
| [Deploy Cloud Stack in AWS](../cloud/docs/deploy-cloud-stack.md) | Provision EC2 infrastructure for Linux/Windows demos |
| [OpenShift CNV](../openshift/docs/openshift-cnv.md) | Run VMs on an existing OpenShift cluster |

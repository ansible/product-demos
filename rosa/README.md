# ROSA Demos

## About These Demos

This category demonstrates automated ROSA (Red Hat OpenShift Service on AWS) cluster lifecycle management through Ansible Automation Platform. Unlike the [OpenShift](../openshift/README.md) demos which assume a cluster already exists, these demos provision and destroy the cluster itself.

### Workflows

| Workflow | Description |
|----------|-------------|
| [**ROSA Cluster Lifecycle (Create)**](docs/rosa-lifecycle.md) | End-to-end cluster creation: preflight checks, account role setup, EIP management, cluster creation, and readiness verification with destroy-on-failure safety path |
| **ROSA Cluster Lifecycle (Destroy)** | Safe cluster teardown with operator role and OIDC provider cleanup (idempotent) |

### Jobs

| Job Template | Description |
|--------------|-------------|
| **ROSA ǀ Preflight Checks** | Validates AWS credentials, ROSA token, IAM permissions, service quotas, EIP availability, and cluster name conflicts |
| **ROSA ǀ Create Cluster** | Creates account roles, frees EIP quota if needed, and initiates STS-mode ROSA cluster creation |
| **ROSA ǀ Wait for Ready** | Polls cluster status until ready (~30-40 min), then creates cluster-admin credentials |
| **ROSA ǀ Destroy Cluster** | Destroys the cluster, STS operator roles, and OIDC provider; safe to run if cluster is already gone |

## Post Setup

After running `APD | Single demo setup` with `demo: rosa`:

### Configure Credentials

1. **AWS** — Add Access Key and Secret Key to the `AWS` credential (same as Cloud demos)
2. **ROSA Token** — Navigate to Resources → Credentials → `ROSA Token` and paste your offline token from https://console.redhat.com/openshift/token/rosa (click "use API tokens to authenticate")

### Execution Environment

The `ROSA Lifecycle EE` image must be accessible from your AAP instance:

```
podman pull quay.io/acme_corp/rosa-ee:latest
```

This image includes `rosa`, `aws`, `oc`, and `jq` CLIs.

## Suggested Usage

### Create a ROSA Cluster

Launch **ROSA ǀ Lifecycle (Create)** workflow and fill the survey:

| Prompt | Purpose |
|--------|---------|
| **Cluster Name** | Must follow `apd-rosa-<purpose>` convention |
| **AWS Region** | Target region (ensure quota availability) |
| **Compute Nodes** | 2 for demos (minimum cost) |
| **Machine Type** | m5.xlarge is sufficient for demos |
| **OpenShift Version** | Leave blank for latest |
| **Cluster TTL** | Tag for cost tracking (e.g. `4h`) |
| **Owner Tag** | Your identifier for cost attribution |

**Timeline:** ~35-45 minutes total. Plan presentations accordingly.

### Destroy a ROSA Cluster

Launch **ROSA ǀ Lifecycle (Destroy)** workflow with the same cluster name and region.

**Timeline:** ~15-25 minutes.

### Cost Warning

| Resource | Cost |
|----------|------|
| ROSA control plane | $0.171/hour |
| m5.xlarge × 2 nodes | ~$0.384/hour |
| **Total** | **~$0.55/hour** |
| **4-hour demo** | **~$2.22** |
| **Forgotten overnight** | **~$6.66** |

**Always destroy clusters after demos.**

## Known Issues

- ROSA offline API tokens are being deprecated; future versions will use Red Hat service account authentication
- The `rosa create account-roles` step recreates IAM roles on each run (harmless but verbose)
- EIP quota release only frees unassociated addresses; if all EIPs are in use, manual release or quota increase is required

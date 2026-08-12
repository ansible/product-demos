# ROSA Lifecycle Demo — Operator Runbook

## Overview

This demo showcases automated Red Hat OpenShift Service on AWS (ROSA) cluster lifecycle management via Ansible Automation Platform (AAP). It provides a complete create-to-destroy cycle suitable for live demonstrations.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           ROSA | Lifecycle (Create) Workflow             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────┐  │
│  │  Preflight   │───▶│    Create    │───▶│   Wait   │  │
│  │   Checks     │    │   Cluster    │    │ for Ready│  │
│  └──────┬───────┘    └──────┬───────┘    └────┬─────┘  │
│         │ fail              │ fail             │ fail   │
│         ▼                   ▼                  ▼        │
│  ┌──────────────┐    ┌──────────────────────────────┐   │
│  │  Feedback:   │    │   Destroy on Failure          │   │
│  │  Preflight   │    │   (cleanup, then feedback)    │   │
│  │  Failed      │    └──────────────────────────────┘   │
│  └──────────────┘                                       │
└─────────────────────────────────────────────────────────┘
```

## Credential Setup

### 1. AWS Credential (Amazon Web Services type)

The standard AWS credential used by other Cloud demos. Must have permissions for:
- EC2 (instances, VPCs, subnets, security groups, EIPs)
- IAM (create/delete roles, policies, OIDC providers)
- ELB (load balancers for cluster ingress)
- CloudFormation (ROSA uses CF stacks)
- STS (AssumeRole for ROSA STS mode)
- Route53 (if using custom domains)

**Minimum IAM policy**: Use the [ROSA STS required policies](https://docs.openshift.com/rosa/rosa_planning/rosa-sts-aws-prereqs.html#rosa-sts-aws-requirements-minimum_rosa-sts-aws-prereqs) from Red Hat documentation.

**In AAP**: Navigate to Resources → Credentials → `AWS`. Set Access Key and Secret Key.

### 2. ROSA Token Credential (custom type)

| Field | Value |
|-------|-------|
| Credential Type | ROSA Token |
| ROSA API Token | Obtain from https://console.redhat.com/openshift/token/rosa |

**In AAP**: Resources → Credentials → Create → Type: `ROSA Token` → paste token.

Token expiration: Tokens are long-lived but check [Red Hat's documentation](https://console.redhat.com/openshift/token/rosa) for renewal procedures.

### 3. Execution Environment

The `ROSA Lifecycle EE` must be available on AAP. It is registered during demo setup but the image must be pre-built and pushed:

```
quay.io/acme_corp/rosa-ee:latest
```

See [Execution Environment Build Instructions](#building-the-execution-environment) below.

## Launch Sequence (AAP UI)

### Creating a Cluster

1. Navigate to **Resources → Templates**
2. Find **ROSA | Lifecycle (Create)** workflow
3. Click **Launch** (rocket icon)
4. Fill the survey:
   - **Cluster Name**: `apd-rosa-demo` (or custom, following naming convention)
   - **AWS Region**: Select target region
   - **Compute Nodes**: `2` for demos (minimum cost)
   - **Machine Type**: `m5.xlarge` (sufficient for demos)
   - **OpenShift Version**: Leave blank for latest
   - **Cluster TTL**: `4h` (tag only; set reminder to destroy)
   - **Owner Tag**: Your identifier
5. Click **Launch**
6. Monitor workflow visualization for progress

**Expected timeline**: ~35-45 minutes total
- Preflight: 1-2 minutes
- Create initiation: 1-2 minutes
- Wait for ready: 30-40 minutes

### Destroying a Cluster

1. Navigate to **Resources → Templates**
2. Find **ROSA | Lifecycle (Destroy)** workflow
3. Click **Launch**
4. Confirm the cluster name and region match what was created
5. Click **Launch**

**Expected timeline**: ~15-25 minutes

## Expected Timings

| Phase | Duration | Notes |
|-------|----------|-------|
| Preflight checks | 1-2 min | Fast fail if issues exist |
| Cluster creation (initiate) | 1-2 min | API call only |
| Cluster ready (wait) | 30-40 min | ROSA control plane + compute |
| Cluster destruction | 10-20 min | Includes role/OIDC cleanup |
| **Total create cycle** | **~35-45 min** | Plan presentations accordingly |
| **Total destroy cycle** | **~15-25 min** | |

## Cost Estimates

| Resource | Approximate Cost |
|----------|-----------------|
| ROSA control plane | $0.171/hour |
| m5.xlarge (per node) | ~$0.192/hour |
| 2-node cluster total | ~$0.555/hour |
| **4-hour demo** | **~$2.22** |
| **Forgotten overnight (12h)** | **~$6.66** |

**Critical**: Always destroy clusters after demos. Set calendar reminders.

## Naming Convention

All ROSA clusters created by this demo must follow:

```
apd-rosa-<purpose>
```

Examples:
- `apd-rosa-demo` — standard demo cluster
- `apd-rosa-summit` — event-specific cluster
- `apd-rosa-test` — testing/validation

## Tagging Strategy

Every cluster is tagged with:

| Tag | Value | Purpose |
|-----|-------|---------|
| `owner` | Survey input | Cost attribution |
| `managed-by` | `aap-product-demos` | Identifies automation-managed resources |
| `ttl` | Survey input (e.g., `4h`) | Expected lifetime for cleanup audits |

## Safety Guardrails

1. **Preflight gate**: Cluster creation cannot proceed without passing all checks
2. **Destroy on failure**: If creation or readiness fails, automatic destroy is triggered
3. **Idempotent destroy**: Safe to re-run destroy even if cluster is already gone
4. **STS mode**: No long-lived IAM credentials stored in the cluster
5. **Naming convention**: Prevents accidental targeting of production clusters
6. **TTL tags**: Enable automated cost-control audits

## Troubleshooting

### Preflight Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `Missing required variables` | Survey not filled or credential not attached | Verify credential attachments on job template |
| `AWS STS get-caller-identity failed` | Invalid/expired AWS credentials | Update AWS credential in AAP |
| `rosa login failed` | Invalid/expired ROSA token | Regenerate at console.redhat.com/openshift/token/rosa |
| `rosa verify permissions` failed | IAM policy too restrictive | Apply ROSA minimum IAM policy |
| `rosa verify quota` failed | AWS service quota exceeded | Request quota increase in AWS console |
| `Cluster already exists` | Name conflict | Destroy existing cluster or use different name |

### Creation Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `OCM account not eligible` | ROSA not enabled on RH account | Enable ROSA at console.redhat.com |
| `Insufficient quota for... ` | EC2/ELB/VPC limits | Increase AWS quotas |
| `Error creating network` | VPC/subnet CIDR conflicts | Try different region or clean up VPCs |
| Timeout during wait | Cluster stuck in `installing` | Check ROSA console; may need manual delete |

### Destruction Failures

| Error | Cause | Fix |
|-------|-------|-----|
| `Cluster not found` | Already deleted (safe) | No action needed |
| Timeout during destroy poll | AWS resources stuck deleting | Check CloudFormation in AWS console |
| Operator role cleanup failed | Roles already removed | Safe to ignore |
| OIDC cleanup failed | Provider already removed | Safe to ignore |

### Orphaned Resource Checklist

If a cluster creation or destruction fails partway, check AWS console for:

- [ ] **CloudFormation stacks** matching the cluster name
- [ ] **IAM roles** with prefix matching cluster ID
- [ ] **OIDC providers** in IAM → Identity providers
- [ ] **VPCs** tagged with `kubernetes.io/cluster/<name>`
- [ ] **Elastic IPs** in the cluster's region
- [ ] **Load Balancers** (NLB/ALB) from ingress
- [ ] **S3 buckets** (OIDC configuration bucket)
- [ ] **Route53 hosted zones** (if custom domain used)

Use `rosa delete cluster --cluster=<name> --best-effort` for stuck deletions.

## Building the Execution Environment

From the `execution_environments/` directory:

```bash
# Prerequisites
podman login registry.redhat.io
export ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN="<token>"
export ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN="<token>"

# Build
./build-rosa.sh

# Verify tools inside the EE
podman run --rm quay.io/acme_corp/rosa-ee:latest rosa version
podman run --rm quay.io/acme_corp/rosa-ee:latest aws --version
podman run --rm quay.io/acme_corp/rosa-ee:latest oc version --client
podman run --rm quay.io/acme_corp/rosa-ee:latest jq --version

# Push to registry
podman manifest push --all quay.io/acme_corp/rosa-ee:<tag>
podman manifest push --all quay.io/acme_corp/rosa-ee:latest
```

## Smoke Test Commands (inside EE)

```bash
# Run interactively inside the EE
podman run --rm -it quay.io/acme_corp/rosa-ee:latest bash

# Verify all required tools
rosa version
aws --version
oc version --client
jq --version
python3.12 -c "import boto3; print(boto3.__version__)"

# Verify ansible and collections
ansible --version
ansible-galaxy collection list | grep -E "amazon.aws|ansible.utils"
```

## Demo Setup in AAP

After the EE is built and pushed, run the standard APD setup:

```bash
ansible-navigator run setup_demo.yml \
  -e demo=rosa \
  --pae false \
  --mode stdout \
  --eei quay.io/ansible-product-demos/apd-ee-26:latest
```

Or select **rosa** in the AAP **APD | Single demo setup** job template survey.

This creates:
- ROSA Token credential type and placeholder credential
- ROSA Lifecycle EE definition
- All 4 job templates
- Both lifecycle workflows

## Cleanup Verification Checklist

After destroying a cluster, verify:

- [ ] `rosa list clusters` shows no matching cluster
- [ ] AWS CloudFormation → no stacks with cluster name
- [ ] AWS IAM → Roles → no `<cluster-name>-*` roles
- [ ] AWS IAM → Identity providers → no matching OIDC
- [ ] AWS VPC → no orphaned VPCs with cluster tags
- [ ] AWS EC2 → no orphaned instances
- [ ] AWS ELB → no orphaned load balancers

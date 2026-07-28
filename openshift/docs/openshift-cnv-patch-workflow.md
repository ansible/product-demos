---
layout: demo-detail
demo_slug: openshift-cnv-patch-workflow
---

Patching workflow for RHEL VMs running on OpenShift Virtualization. Similar to the cloud patching workflow but targeting CNV-managed virtual machines instead of EC2 instances.

## Prerequisites

- RHEL VMs provisioned on OpenShift CNV
- <strong>OpenShift Credential</strong> configured
- SSH connectivity to the CNV VMs

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ CNV ǀ Patch Workflow | [`openshift/setup.yml`](https://github.com/ansible/product-demos/blob/main/openshift/setup.yml) | Runs the patching workflow against CNV-managed RHEL virtual machines |

## Related demos

| Demo | Description |
|------|-------------|
| 🩹 [Patch Cloud Stack in AWS](/product-demos/demos/patch-cloud-stack/) | The AWS version of this patching workflow |
| ⎈ [CNV — Infra Stack](/product-demos/demos/openshift-cnv-infra-stack/) | Deploy the CNV infrastructure to patch |

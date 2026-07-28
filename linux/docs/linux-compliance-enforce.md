---
layout: demo-detail
demo_slug: linux-compliance-enforce
---

Applies remediation for a compliance profile (CIS, HIPAA, OSPP, PCI-DSS, or STIG) to hosts that were found out of compliance. Targets hosts dynamically based on inventory groups populated by a prior compliance scan.

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- A prior compliance scan that populated the out-of-compliance inventory group

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX | Compliance Enforce | [`linux/remediate_out_of_compliance.yml`](https://github.com/ansible/product-demos/blob/main/linux/remediate_out_of_compliance.yml) | Applies compliance role remediation to hosts in the OUT_OF_COMPLIANCE group |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Compliance Workflow](/product-demos/demos/linux-compliance-workflow/) | Full workflow that combines scanning, inventory sync, and enforcement |
| 🐧 [Multi-profile Compliance Report](/product-demos/demos/linux-compliance-report/) | Generate a compliance report to measure the impact of enforcement |

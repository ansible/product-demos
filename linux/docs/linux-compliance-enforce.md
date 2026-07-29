# Compliance Enforce


Applies remediation for a compliance profile (CIS, HIPAA, OSPP, PCI-DSS, or STIG) to hosts that were found out of compliance. Targets hosts dynamically based on inventory groups populated by a prior compliance scan.

## Prerequisites

- RHEL hosts in the **Ansible Product Demos Inventory**
- A prior compliance scan that populated the out-of-compliance inventory group


## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Compliance Enforce | [`linux/remediate_out_of_compliance.yml`](../remediate_out_of_compliance.yml) | Applies compliance role remediation to hosts in the OUT_OF_COMPLIANCE group |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Compliance Workflow](./linux-compliance-workflow.md) | Full workflow that combines scanning, inventory sync, and enforcement |
| 🐧 [Multi-profile Compliance Report](./linux-compliance-report.md) | Generate a compliance report to measure the impact of enforcement |

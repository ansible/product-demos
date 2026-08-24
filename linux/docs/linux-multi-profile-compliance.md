# Multi-profile Compliance


Applies a selected compliance profile (CIS, HIPAA, OSPP, PCI-DSS, or STIG) to RHEL hosts using the official Red Hat compliance roles. This is the enforcement-only playbook -- for scanning and reporting, see the Multi-profile Compliance Report.

## Prerequisites

- RHEL hosts in the **Ansible Product Demos Inventory**
- SSH connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Compliance Profile | `compliance_profile` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Multi-profile Compliance | [`linux/multi_profile_compliance.yml`](../multi_profile_compliance.yml) | Applies the selected compliance profile to target hosts |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Multi-profile Compliance Report](./linux-compliance-report.md) | Generate an OpenSCAP report to assess compliance posture |
| 🐧 [Compliance Workflow](./linux-compliance-workflow.md) | Automated scan then enforce workflow |

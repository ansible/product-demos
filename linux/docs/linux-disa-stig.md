# DISA STIG


Applies DISA STIG (Security Technical Implementation Guide) hardening to RHEL hosts. Uses the demo.compliance collection STIG role to configure security controls required for U.S. Department of Defense environments.

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ DISA STIG | [`linux/disa_stig.yml`](../disa_stig.yml) | Applies DISA STIG hardening controls from the demo.compliance collection |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Compliance Workflow](./linux-compliance-workflow.md) | Full compliance workflow with scanning and enforcement |
| 🐧 [Multi-profile Compliance Report](./linux-compliance-report.md) | Generate a compliance report to measure STIG compliance |

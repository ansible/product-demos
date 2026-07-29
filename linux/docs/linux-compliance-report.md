# Multi-profile Compliance Report


Runs an OpenSCAP scan against a selected compliance profile and generates an HTML report. Installs the scanner and security guide packages, evaluates the system against the profile, and publishes results as a browsable HTML report.

## Prerequisites

- RHEL hosts with at least 2 GB RAM
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Compliance Profile | `compliance_profile` | multiplechoice | Yes |
| Use httpd to host reports locally? | `use_httpd` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Multi-profile Compliance Report | [`linux/multi_profile_compliance_report.yml`](../multi_profile_compliance_report.yml) | Runs OpenSCAP scan and generates an HTML compliance report on target hosts |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Multi-profile Compliance](./linux-multi-profile-compliance.md) | Apply compliance enforcement after reviewing the report |
| 🐧 [Compliance Workflow](./linux-compliance-workflow.md) | Automated scan then enforce workflow that uses this report |

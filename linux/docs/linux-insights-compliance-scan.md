# Insights Compliance Scan


Triggers a Red Hat Insights compliance scan on RHEL hosts. Uses the redhat.insights.compliance role to run the scan and upload results to the Insights compliance dashboard on console.redhat.com.

## Prerequisites

- RHEL hosts registered with Red Hat Insights
- Compliance profile assigned in Insights

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Compliance profile configured? | `compliance_profile_configured` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Insights Compliance Scan | [`linux/insights_compliance_scan.yml`](../insights_compliance_scan.yml) | Runs the Insights compliance scan and uploads results to console.redhat.com |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Register with Insights](./linux-register-insights.md) | Register hosts with RHSM before running Insights scans |
| 🐧 [Multi-profile Compliance Report](./linux-compliance-report.md) | Local OpenSCAP scanning as an alternative to Insights |

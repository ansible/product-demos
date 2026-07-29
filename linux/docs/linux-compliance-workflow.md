# Compliance Workflow


A workflow that ties together compliance reporting, inventory refresh, and enforcement in a single execution. It first generates an OpenSCAP report against a chosen compliance profile (CIS, HIPAA, OSPP, PCI-DSS, or STIG), syncs the AWS inventory, and then enforces remediation on findings — giving you a before-and-after view of compliance posture.

## Workflow

```
Compliance Report ──→ Update Inventory ──→ Compliance Enforce
```

1. **Compliance Report** — Runs an OpenSCAP scan against the chosen profile and generates an HTML report
2. **Update Inventory** — Syncs the AWS dynamic inventory to refresh host groups
3. **Compliance Enforce** — Remediates out-of-compliance findings from the scan

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>
- AWS credential configured (for inventory sync step)
- (Recommended) Run <strong>Deploy Cloud Stack in AWS</strong> first to create target VMs

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Compliance Profile | `compliance_profile` | multiplechoice | Yes |
| Use httpd on the target host(s) to access reports locally? | `use_httpd` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Multi-profile Compliance Report | [`linux/multi_profile_compliance_report.yml`](https://github.com/ansible/product-demos/blob/main/linux/multi_profile_compliance_report.yml) | Runs an OpenSCAP scan against the selected compliance profile and generates an HTML report |
| AWS Inventory | [`(inventory sync)`](https://github.com/ansible/product-demos/blob/main/(inventory sync)) | Refreshes the AWS dynamic inventory to ensure host data is current before enforcement |
| LINUX ǀ Compliance Enforce | [`linux/remediate_out_of_compliance.yml`](https://github.com/ansible/product-demos/blob/main/linux/remediate_out_of_compliance.yml) | Applies remediation for findings from the compliance scan |

## Why it matters

- Compliance is a board-level concern — this demo shows automated enforcement, not just reporting
- The scan-then-enforce pattern mirrors real-world change management workflows
- Supporting five compliance profiles (CIS, HIPAA, OSPP, PCI-DSS, STIG) covers most regulated industries
- Inventory sync between scan and enforce ensures AAP is working with current host data
- The workflow structure makes the process auditable and repeatable

## Presenter walkthrough

1. <strong>Choose a profile:</strong> Show the survey and explain the compliance profile options. 'CIS and STIG are the most common — pick one that matches your audience.'
2. <strong>Launch the workflow:</strong> Start the workflow and show the three-node chain: Report → Inventory Sync → Enforce.
3. <strong>Review the initial report:</strong> While the workflow runs, explain that the first node scans and generates an HTML report. 'This is our baseline — here is where we stand before remediation.'
4. <strong>Inventory sync:</strong> Point out the middle node. 'We refresh inventory between scan and enforce to make sure we are working with the latest host data.'
5. <strong>Enforcement results:</strong> After completion, show the enforce job output. Highlight specific remediation tasks that changed. 'Each of these is a compliance control being applied automatically.'
6. <strong>Re-run the report:</strong> For maximum impact, re-run just the compliance report template and compare before and after scores.

## Talking points

- This is not just scanning — it is automated remediation. The workflow finds problems and fixes them.
- Five compliance profiles cover most regulated industries: finance (PCI-DSS), healthcare (HIPAA), government (STIG, OSPP), and general best practices (CIS).
- The scan-sync-enforce pattern is how enterprises actually implement compliance. This demo mirrors that real-world workflow.
- Running the report before and after enforcement gives you a measurable delta — perfect for auditors and compliance officers.

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Multi-profile Compliance](/product-demos/demos/linux-multi-profile-compliance/) | Run the compliance report standalone to assess posture without enforcing |
| 🐧 [DISA STIG](/product-demos/demos/linux-disa-stig/) | Apply DISA STIG hardening directly without the workflow wrapper |
| 🐧 [Patching](/product-demos/demos/linux-patching/) | Patch first, then run compliance to show a complete day-2 operations story |

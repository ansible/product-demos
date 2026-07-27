---
layout: demo-detail
demo_slug: linux-compliance-workflow
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
  - "AWS credential configured (for inventory sync step)"
  - "(Recommended) Run <strong>Deploy Cloud Stack in AWS</strong> first to create target VMs"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Compliance Profile"
    variable: compliance_profile
    type: multiplechoice
    required: "Yes"
  - question: "Use httpd on the target host(s) to access reports locally?"
    variable: use_httpd
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "LINUX | Multi-profile Compliance Report"
    playbook: linux/multi_profile_compliance_report.yml
    description: "Runs an OpenSCAP scan against the selected compliance profile and generates an HTML report"
  - name: "AWS Inventory"
    playbook: (inventory sync)
    description: "Refreshes the AWS dynamic inventory to ensure host data is current before enforcement"
  - name: "LINUX | Compliance Enforce"
    playbook: linux/remediate_out_of_compliance.yml
    description: "Applies remediation for findings from the compliance scan"
related_demos:
  - slug: linux-multi-profile-compliance
    description: "Run the compliance report standalone to assess posture without enforcing"
  - slug: linux-disa-stig
    description: "Apply DISA STIG hardening directly without the workflow wrapper"
  - slug: linux-patching
    description: "Patch first, then run compliance to show a complete day-2 operations story"
---

A workflow that ties together compliance reporting, inventory refresh, and enforcement in a single execution. It first generates an OpenSCAP report against a chosen compliance profile (CIS, HIPAA, OSPP, PCI-DSS, or STIG), syncs the AWS inventory, and then enforces remediation on findings — giving you a before-and-after view of compliance posture.

_Scan, sync, and enforce compliance in one automated workflow_

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

---
layout: demo-detail
demo_slug: linux-multi-profile-compliance
description: >-
  Applies a selected compliance profile (CIS, HIPAA, OSPP, PCI-DSS, or STIG)
  to RHEL hosts using the official Red Hat compliance roles. This is the
  enforcement-only playbook -- for scanning and reporting, see the
  Multi-profile Compliance Report.
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Compliance Profile"
    variable: compliance_profile
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "LINUX | Multi-profile Compliance"
    playbook: linux/multi_profile_compliance.yml
    description: "Applies the selected compliance profile to target hosts"
related_demos:
  - slug: linux-compliance-report
    description: "Generate an OpenSCAP report to assess compliance posture"
  - slug: linux-compliance-workflow
    description: "Automated scan then enforce workflow"
---

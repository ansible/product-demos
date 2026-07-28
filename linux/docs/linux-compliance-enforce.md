---
layout: demo-detail
demo_slug: linux-compliance-enforce
description: >-
  Applies remediation for a compliance profile (CIS, HIPAA, OSPP, PCI-DSS, or
  STIG) to hosts that were found out of compliance. Targets hosts dynamically
  based on inventory groups populated by a prior compliance scan.
prerequisites:
  - "RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "A prior compliance scan that populated the out-of-compliance inventory group"
job_templates:
  - name: "LINUX | Compliance Enforce"
    playbook: linux/remediate_out_of_compliance.yml
    description: "Applies compliance role remediation to hosts in the OUT_OF_COMPLIANCE group"
related_demos:
  - slug: linux-compliance-workflow
    description: "Full workflow that combines scanning, inventory sync, and enforcement"
  - slug: linux-compliance-report
    description: "Generate a compliance report to measure the impact of enforcement"
---

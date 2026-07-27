---
layout: demo-detail
demo_slug: windows-rollback
prerequisites:
  - "Windows hosts in the <strong>Ansible Product Demos Inventory</strong>"
job_templates:
  - name: "WINDOWS | Rollback"
    playbook: windows/rollback.yml
    description: "Outputs rollback message -- used as a failure handler in workflows"
related_demos:
  - slug: windows-setup-ad-domain
    description: "Uses this playbook as its failure cleanup handler"
---

A generic rollback playbook used as a cleanup step in Windows workflows. Outputs a configurable rollback message. Used by the Setup Active Directory Domain workflow as the failure handler to clean up resources on error.

_Generic workflow rollback and cleanup step_

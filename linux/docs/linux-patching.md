---
layout: demo-detail
demo_slug: linux-patching
description: >-
  Apply security updates to RHEL servers and generate an HTML patch report.
  The playbook installs yum-utils, applies patches via the
  demo.patching.patch_linux role, optionally triggers an Insights Client scan,
  and publishes a patching compliance report to a dedicated report server.
  Runs in check mode by default so you can audit before applying.
prerequisites:
  - "Linux hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
  - "A host named <code>reports</code> in inventory to receive the HTML report (deployed by <strong>Deploy Cloud Stack in AWS</strong>)"
  - "(Optional) Insights Client configured on target hosts for post-patch scanning"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
related_demos:
  - slug: patch-cloud-stack
    description: "Full enterprise patching workflow with snapshots, parallel RHEL/Windows paths, and automatic rollback"
  - slug: linux-register-insights
    description: "Register hosts with Red Hat Insights for advisory visibility and dynamic inventory"
  - slug: linux-multi-profile-compliance
    description: "Run an OpenSCAP report to assess security posture before and after patching"
---

## Why it matters

- Patching is the number one use case customers ask about — this demo addresses it directly
- Check mode lets you show a safe audit-first workflow before committing changes
- The HTML report gives stakeholders a tangible artifact without a separate CMDB integration
- Insights Client integration shows how AAP and Red Hat Insights work together for visibility
- Demonstrates role-based content reuse with the demo.patching collection

## Presenter walkthrough

1. <strong>Explain check mode:</strong> Show the audience that this template defaults to check mode. 'We can audit what would change before we touch a single package.'
2. <strong>Launch in check mode:</strong> Run against a group of RHEL hosts. Walk through the output — which packages would be updated, which hosts are already current.
3. <strong>Switch to run mode:</strong> Re-launch the job and change the job type to Run. 'Now we apply the patches for real — same playbook, same survey, different intent.'
4. <strong>Show the report:</strong> Navigate to the reports server and open the patching report. Walk through the per-host breakdown of applied updates.
5. <strong>Insights integration:</strong> If Insights Client is configured, show how the post-patch scan updates the host profile in Red Hat Insights automatically.
6. <strong>Connect to the bigger picture:</strong> 'For a full enterprise workflow with snapshots and rollback, check out Patch Cloud Stack in AWS.'

## Talking points

- Check mode versus run mode is a powerful pattern — audit first, patch second, all from the same template.
- The HTML report is generated automatically on every run. Hand it to your change board or attach it to a ticket.
- Insights Client scanning after patching closes the loop — your compliance dashboard updates in near real-time.
- This is a single job template. For heterogeneous environments with Windows, snapshots, and rollback, we have a full workflow demo.

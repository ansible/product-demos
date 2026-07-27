---
layout: demo-detail
demo_slug: satellite-patch-dev
prerequisites:
  - "<strong>Satellite Collection</strong> credential configured"
  - "Content views and lifecycle environments configured in Satellite"
  - "Dev hosts registered with Satellite"
  - "Run <strong>APD | Single demo setup</strong> with <code>satellite</code>"
job_templates:
  - name: "SATELLITE | Patch Dev (workflow)"
    playbook: satellite/setup.yml
    description: "Publishes content view, syncs hosts, and applies patches to development environment"
related_demos:
  - slug: satellite-publish-content-view
    description: "Standalone content view publishing"
  - slug: satellite-promote-content-view
    description: "Promote content from dev to production after testing"
---

End-to-end Satellite patching workflow for development environments. Combines content view publishing with host patching to demonstrate the full content management lifecycle.

_Publish content and patch dev hosts through Satellite_

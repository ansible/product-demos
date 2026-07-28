---
layout: demo-detail
demo_slug: satellite-promote-content-view
description: >-
  Promotes a Satellite content view version from one lifecycle environment to
  another. This is the mechanism for moving tested content from Dev to QA to
  Production in a controlled manner.
prerequisites:
  - "<strong>Satellite Collection</strong> credential configured"
  - "A published content view version to promote"
survey_prompts:
  - question: "Content View"
    variable: content_view
    type: text
    required: "Yes"
  - question: "Current Lifecycle Environment"
    variable: current_lifecycle_environment
    type: text
    required: "Yes"
  - question: "Target Lifecycle Environment"
    variable: lifecycle_environment
    type: text
    required: "Yes"
job_templates:
  - name: "SATELLITE | Promote Content View"
    playbook: satellite/satellite_promote.yml
    description: "Promotes a content view version from one lifecycle environment to another"
related_demos:
  - slug: satellite-publish-content-view
    description: "Publish a new version before promoting"
---

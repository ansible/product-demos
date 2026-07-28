---
layout: demo-detail
demo_slug: satellite-publish-content-view
description: >-
  Publishes a new version of a Satellite content view to a specified lifecycle
  environment. Content views control which packages and errata are available
  to hosts -- publishing creates a point-in-time snapshot of the content.
prerequisites:
  - "<strong>Satellite Collection</strong> credential configured"
  - "Content views already defined in Satellite"
survey_prompts:
  - question: "Content View"
    variable: content_view
    type: text
    required: "Yes"
  - question: "Environment"
    variable: env
    type: text
    required: "Yes"
job_templates:
  - name: "SATELLITE | Publish Content View"
    playbook: satellite/satellite_publish.yml
    description: "Publishes a new version of the content view to the specified lifecycle environment"
related_demos:
  - slug: satellite-promote-content-view
    description: "Promote the published version to the next lifecycle stage"
---

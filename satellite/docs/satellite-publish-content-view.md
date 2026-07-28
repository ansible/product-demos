---
layout: demo-detail
demo_slug: satellite-publish-content-view
---

Publishes a new version of a Satellite content view to a specified lifecycle environment. Content views control which packages and errata are available to hosts -- publishing creates a point-in-time snapshot of the content.

## Prerequisites

- <strong>Satellite Collection</strong> credential configured
- Content views already defined in Satellite

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Content View | `content_view` | text | Yes |
| Environment | `env` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| SATELLITE ǀ Publish Content View | [`satellite/satellite_publish.yml`](https://github.com/ansible/product-demos/blob/main/satellite/satellite_publish.yml) | Publishes a new version of the content view to the specified lifecycle environment |

## Related demos

| Demo | Description |
|------|-------------|
| 🛰️ [Promote Content View Version](/product-demos/demos/satellite-promote-content-view/) | Promote the published version to the next lifecycle stage |

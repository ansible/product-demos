# Promote Content View Version


Promotes a Satellite content view version from one lifecycle environment to another. This is the mechanism for moving tested content from Dev to QA to Production in a controlled manner.

## Prerequisites

- <strong>Satellite Collection</strong> credential configured
- A published content view version to promote

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Content View | `content_view` | text | Yes |
| Current Lifecycle Environment | `current_lifecycle_environment` | text | Yes |
| Target Lifecycle Environment | `lifecycle_environment` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| SATELLITE ǀ Promote Content View | [`satellite/satellite_promote.yml`](../satellite_promote.yml) | Promotes a content view version from one lifecycle environment to another |

## Related demos

| Demo | Description |
|------|-------------|
| 🛰️ [Publish Content View Version](./satellite-publish-content-view.md) | Publish a new version before promoting |

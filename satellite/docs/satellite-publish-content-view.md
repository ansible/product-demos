# Publish Content View Version


Publishes a new version of a Satellite content view to a specified lifecycle environment. Content views control which packages and errata are available to hosts -- publishing creates a point-in-time snapshot of the content.

## Prerequisites

- **Satellite Collection** credential configured
- Content views already defined in Satellite

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Content View | `content_view` | text | Yes |
| Environment | `env` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| SATELLITE ǀ Publish Content View | [`satellite/satellite_publish.yml`](../satellite_publish.yml) | Publishes a new version of the content view to the specified lifecycle environment |

## Related demos

| Demo | Description |
|------|-------------|
| 🛰️ [Promote Content View Version](./satellite-promote-content-view.md) | Promote the published version to the next lifecycle stage |

---
layout: demo-detail
demo_slug: satellite-patch-dev
---
# Patch Dev Workflow


End-to-end Satellite patching workflow for development environments. Combines content view publishing with host patching to demonstrate the full content management lifecycle.

## Prerequisites

- <strong>Satellite Collection</strong> credential configured
- Content views and lifecycle environments configured in Satellite
- Dev hosts registered with Satellite
- Run <strong>APD | Single demo setup</strong> with <code>satellite</code>

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| SATELLITE ǀ Patch Dev (workflow) | [`satellite/setup.yml`](https://github.com/ansible/product-demos/blob/main/satellite/setup.yml) | Publishes content view, syncs hosts, and applies patches to development environment |

## Related demos

| Demo | Description |
|------|-------------|
| 🛰️ [Publish Content View Version](/product-demos/demos/satellite-publish-content-view/) | Standalone content view publishing |
| 🛰️ [Promote Content View Version](/product-demos/demos/satellite-promote-content-view/) | Promote content from dev to production after testing |

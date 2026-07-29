# Patch Dev Workflow


End-to-end Satellite patching workflow for development environments. Syncs the Satellite inventory, publishes a new content view version, patches development hosts, and reports results. Demonstrates the full content management lifecycle from content publication through to host remediation.

## Prerequisites

- <strong>Satellite Collection</strong> credential configured
- Content views and lifecycle environments configured in Satellite
- Dev hosts registered with Satellite
- Run <strong>APD | Single demo setup</strong> with <code>satellite</code>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Email | `email` | text | Yes |

## Workflow nodes

| Step | Template | Description |
|------|----------|-------------|
| 1 | Satellite Inventory | Sync Satellite dynamic inventory into AAP |
| 2 | SATELLITE ǀ Publish Content View Version | Publish a new content view version with latest errata |
| 3 | LINUX ǀ Patching | Apply patches to development hosts from the updated content view |
| 4 | SUBMIT FEEDBACK | Send notification email with workflow results |

## Related demos

| Demo | Description |
|------|-------------|
| 🛰️ [Publish Content View Version](./satellite-publish-content-view.md) | Standalone content view publishing |
| 🛰️ [Promote Content View Version](./satellite-promote-content-view.md) | Promote content from dev to production after testing |

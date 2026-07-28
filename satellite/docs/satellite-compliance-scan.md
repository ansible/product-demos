---
layout: demo-detail
demo_slug: satellite-compliance-scan
---

Runs OpenSCAP compliance scans on Satellite-managed hosts and uploads results to Satellite. Uses the demo.satellite.scap_client role to install and configure the foreman_scap_client.

## Prerequisites

- Hosts registered with Satellite
- Compliance policies configured in Satellite
- <strong>Satellite Collection</strong> credential configured

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ OpenSCAP Scan (Satellite) | [`satellite/server_openscap.yml`](https://github.com/ansible/product-demos/blob/main/satellite/server_openscap.yml) | Installs foreman_scap_client, runs compliance scans, and uploads results to Satellite |

## Related demos

| Demo | Description |
|------|-------------|
| 🛰️ [Register with Satellite](/product-demos/demos/satellite-register/) | Register hosts with Satellite before scanning |
| 🐧 [Multi-profile Compliance Report](/product-demos/demos/linux-compliance-report/) | Local OpenSCAP scanning without Satellite |

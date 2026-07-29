---
layout: demo-detail
demo_slug: satellite-register
---
# Register with Satellite


Registers RHEL hosts with a Red Hat Satellite server. Uses the demo.satellite.register_host role to configure the Satellite URL, install the katello-ca-consumer package, and register the host.

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- <strong>Satellite Collection</strong> credential configured
- Run <strong>APD | Single demo setup</strong> with <code>satellite</code>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Register with Satellite | [`satellite/server_register.yml`](https://github.com/ansible/product-demos/blob/main/satellite/server_register.yml) | Registers target RHEL hosts with the configured Satellite server |

## Related demos

| Demo | Description |
|------|-------------|
| 🛰️ [Compliance Scan with Satellite](/product-demos/demos/satellite-compliance-scan/) | Run compliance scans on Satellite-managed hosts |
| 🐧 [Register with Insights](/product-demos/demos/linux-register-insights/) | Register directly with RHSM instead of through Satellite |

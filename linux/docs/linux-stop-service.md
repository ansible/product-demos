---
layout: demo-detail
demo_slug: linux-stop-service
---
# Stop Service


Stops a named systemd service on target hosts. Checks that the service exists before attempting to stop it. Paired with Start Service for basic service lifecycle management.

## Prerequisites

- Linux hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Service Name | `service_name` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Stop Service | [`linux/service_stop.yml`](https://github.com/ansible/product-demos/blob/main/linux/service_stop.yml) | Checks for the service and stops it if present |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Start Service](/product-demos/demos/linux-start-service/) | Start a stopped service |

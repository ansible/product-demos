---
layout: demo-detail
demo_slug: linux-start-service
---

Starts a named systemd service on target hosts. Checks that the service exists before attempting to start it. A simple but common operational task that demonstrates self-service IT operations.

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
| LINUX | Start Service | [`linux/service_start.yml`](https://github.com/ansible/product-demos/blob/main/linux/service_start.yml) | Checks for the service and starts it if present |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Stop Service](/product-demos/demos/linux-stop-service/) | Stop a running service |

# Start Service


Starts a named systemd service on target hosts. Checks that the service exists before attempting to start it. A simple but common operational task that demonstrates self-service IT operations.

## Prerequisites

- Linux hosts in the **Ansible Product Demos Inventory**
- SSH connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Service Name | `service_name` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Start Service | [`linux/service_start.yml`](../service_start.yml) | Checks for the service and starts it if present |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Stop Service](./linux-stop-service.md) | Stop a running service |

# Deploy Application


Installs a Linux application package via DNF. Supports version pinning with allow_downgrade for rollback scenarios. A straightforward demo of application deployment that shows how AAP replaces manual package management.

## Prerequisites

- Linux hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Application | `application` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Deploy Application | [`linux/deploy_application.yml`](../deploy_application.yml) | Installs or updates an application package via DNF on target hosts |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Podman Webserver](./linux-podman-webserver.md) | Container-based deployment as an alternative to packages |

---
layout: demo-detail
demo_slug: linux-deploy-application
---

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
| LINUX | Deploy Application | [`linux/deploy_application.yml`](https://github.com/ansible/product-demos/blob/main/linux/deploy_application.yml) | Installs or updates an application package via DNF on target hosts |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Podman Webserver](/product-demos/demos/linux-podman-webserver/) | Container-based deployment as an alternative to packages |

---
layout: demo-detail
demo_slug: linux-podman-webserver
---

Deploys a containerized Apache httpd webserver using Podman. Installs Podman, creates a volume directory with a custom index.html, and runs an httpd container serving the custom page. Demonstrates rootless container management with Ansible.

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Web Page Message | `message` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Podman Webserver | [`linux/podman.yml`](https://github.com/ansible/product-demos/blob/main/linux/podman.yml) | Installs Podman, creates a custom index.html, and runs an httpd container |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Deploy Application](/product-demos/demos/linux-deploy-application/) | Traditional package-based application deployment |

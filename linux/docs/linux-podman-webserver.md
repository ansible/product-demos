# Podman Webserver


Deploys a containerized Apache httpd webserver using Podman. Installs Podman, creates a volume directory with a custom index.html, and runs an httpd container serving the custom page. Demonstrates rootless container management with Ansible.

## Prerequisites

- RHEL hosts in the **Ansible Product Demos Inventory**
- SSH connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Web Page Message | `message` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Podman Webserver | [`linux/podman.yml`](../podman.yml) | Installs Podman, creates a custom index.html, and runs an httpd container |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Deploy Application](./linux-deploy-application.md) | Traditional package-based application deployment |

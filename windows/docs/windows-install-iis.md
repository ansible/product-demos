---
layout: demo-detail
demo_slug: windows-install-iis
---
# Install IIS


Installs Internet Information Services (IIS) on Windows Server, starts the W3SVC service, and deploys a custom index.html page. The page content is provided via survey. A quick, visual demo of Windows application deployment with Ansible.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong>
- WinRM connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| IIS Message | `iis_message` | textarea | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Install IIS | [`windows/install_iis.yml`](https://github.com/ansible/product-demos/blob/main/windows/install_iis.yml) | Installs the IIS Web-Server feature, starts it, and deploys a custom index page |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Patching](/product-demos/demos/windows-patching/) | Patch Windows hosts after deploying applications |
| 🪟 [Test Connectivity](/product-demos/demos/windows-test-connectivity/) | Verify WinRM is working before running demos |

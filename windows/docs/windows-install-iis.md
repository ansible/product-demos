# Install IIS


Installs Internet Information Services (IIS) on Windows Server, starts the W3SVC service, and deploys a custom index.html page. The page content is provided via survey. A quick, visual demo of Windows application deployment with Ansible.

## Prerequisites

- Windows hosts in the **Ansible Product Demos Inventory**
- WinRM connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| IIS Message | `iis_message` | textarea | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Install IIS | [`windows/install_iis.yml`](../install_iis.yml) | Installs the IIS Web-Server feature, starts it, and deploys a custom index page |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Patching](./windows-patching.md) | Patch Windows hosts after deploying applications |
| 🪟 [Test Connectivity](./windows-test-connectivity.md) | Verify WinRM is working before running demos |

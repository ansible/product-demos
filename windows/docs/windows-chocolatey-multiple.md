# Chocolatey Install Multiple


Installs multiple packages (Node.js and Python by default) using the Chocolatey package manager. Verifies the installations by checking version output. Demonstrates bulk software provisioning on Windows with Ansible.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong>
- WinRM connectivity via <strong>APD Machine Credential</strong>
- Internet access from the Windows hosts


## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | No |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Chocolatey Install Multiple | [`windows/windows_choco_multiple.yml`](https://github.com/ansible/product-demos/blob/main/windows/windows_choco_multiple.yml) | Installs Node.js and Python via Chocolatey and verifies the installed versions |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Chocolatey Install Specific](/product-demos/demos/windows-chocolatey-specific/) | Install a single specific package via Chocolatey |
| 🪟 [Install IIS](/product-demos/demos/windows-install-iis/) | Install IIS using native Windows features instead of Chocolatey |

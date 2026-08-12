# Chocolatey Install Multiple


Installs multiple packages (Node.js and Python by default) using the Chocolatey package manager. Verifies the installations by checking version output. Demonstrates bulk software provisioning on Windows with Ansible.

## Prerequisites

- Windows hosts in the **Ansible Product Demos Inventory**
- WinRM connectivity via **APD Machine Credential**
- Internet access from the Windows hosts


## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | No |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Chocolatey Install Multiple | [`windows/windows_choco_multiple.yml`](../windows_choco_multiple.yml) | Installs Node.js and Python via Chocolatey and verifies the installed versions |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Chocolatey Install Specific](./windows-chocolatey-specific.md) | Install a single specific package via Chocolatey |
| 🪟 [Install IIS](./windows-install-iis.md) | Install IIS using native Windows features instead of Chocolatey |

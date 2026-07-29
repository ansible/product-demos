# Chocolatey Install Specific


Installs a specific package by name using the Chocolatey package manager. The package name is provided via survey. Demonstrates targeted software installation on Windows.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong>
- WinRM connectivity via <strong>APD Machine Credential</strong>
- Internet access from the Windows hosts

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Package Name | `package_name` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Chocolatey Install Specific | [`windows/windows_choco_specific.yml`](https://github.com/ansible/product-demos/blob/main/windows/windows_choco_specific.yml) | Installs a single named package via Chocolatey |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Chocolatey Install Multiple](/product-demos/demos/windows-chocolatey-multiple/) | Install multiple packages at once |

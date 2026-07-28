---
layout: demo-detail
demo_slug: windows-test-connectivity
---

Tests WinRM connectivity to Windows hosts using wait_for_connection and win_ping. Verifies that AAP can reach the hosts before running any configuration. Useful as a smoke test after provisioning.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong>
- WinRM connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS | Test Connectivity | [`windows/connect.yml`](https://github.com/ansible/product-demos/blob/main/windows/connect.yml) | Waits for WinRM to become available and runs win_ping to confirm connectivity |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Install IIS](/product-demos/demos/windows-install-iis/) | Run a quick demo after confirming connectivity |
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | Deploy Windows VMs to test against |

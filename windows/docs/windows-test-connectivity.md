# Test Connectivity


Tests WinRM connectivity to Windows hosts using wait_for_connection and win_ping. Verifies that AAP can reach the hosts before running any configuration. Useful as a smoke test after provisioning.

## Prerequisites

- Windows hosts in the **Ansible Product Demos Inventory**
- WinRM connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS ǀ Test Connectivity | [`windows/connect.yml`](../connect.yml) | Waits for WinRM to become available and runs win_ping to confirm connectivity |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Install IIS](./windows-install-iis.md) | Run a quick demo after confirming connectivity |
| 🚀 [Deploy Cloud Stack in AWS](../../cloud/docs/deploy-cloud-stack.md) | Deploy Windows VMs to test against |

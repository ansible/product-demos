# Troubleshoot


Gathers quick diagnostic information from RHEL hosts -- vmstat for CPU/memory/swap, top processes by CPU usage, and top processes by memory usage. A handy first-response playbook for investigating performance issues.

## Prerequisites

- Linux hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Troubleshoot | [`linux/tshoot.yml`](https://github.com/ansible/product-demos/blob/main/linux/tshoot.yml) | Runs vmstat, ps by CPU, and ps by memory on target hosts and displays results |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Fact Scan](/product-demos/demos/linux-fact-scan/) | Gather broader system facts including packages and services |
| 🐧 [Run Shell Script](/product-demos/demos/linux-run-shell-script/) | Run ad-hoc commands for deeper investigation |

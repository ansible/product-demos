# Troubleshoot


Gathers quick diagnostic information from RHEL hosts -- vmstat for CPU/memory/swap, top processes by CPU usage, and top processes by memory usage. A handy first-response playbook for investigating performance issues.

## Prerequisites

- Linux hosts in the **Ansible Product Demos Inventory**
- SSH connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Troubleshoot | [`linux/tshoot.yml`](../tshoot.yml) | Runs vmstat, ps by CPU, and ps by memory on target hosts and displays results |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Fact Scan](./linux-fact-scan.md) | Gather broader system facts including packages and services |
| 🐧 [Run Shell Script](./linux-run-shell-script.md) | Run ad-hoc commands for deeper investigation |

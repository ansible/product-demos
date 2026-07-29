# Run Shell Script


Runs an arbitrary shell script on target hosts. The script content is provided via survey. Outputs the result and reminds users they should consider converting scripts to proper playbooks. Great for showing the migration path from scripts to automation.

## Prerequisites

- Linux hosts in the **Ansible Product Demos Inventory**
- SSH connectivity via **APD Machine Credential**

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Shell Script | `shell_script` | textarea | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Run Shell Script | [`linux/run_script.yml`](../run_script.yml) | Executes the provided shell script on target hosts and displays the output |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Troubleshoot](./linux-troubleshoot.md) | Pre-built troubleshooting commands instead of ad-hoc scripts |

---
layout: demo-detail
demo_slug: linux-run-shell-script
---
# Run Shell Script


Runs an arbitrary shell script on target hosts. The script content is provided via survey. Outputs the result and reminds users they should consider converting scripts to proper playbooks. Great for showing the migration path from scripts to automation.

## Prerequisites

- Linux hosts in the <strong>Ansible Product Demos Inventory</strong>
- SSH connectivity via <strong>APD Machine Credential</strong>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Shell Script | `shell_script` | textarea | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Run Shell Script | [`linux/run_script.yml`](https://github.com/ansible/product-demos/blob/main/linux/run_script.yml) | Executes the provided shell script on target hosts and displays the output |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Troubleshoot](/product-demos/demos/linux-troubleshoot/) | Pre-built troubleshooting commands instead of ad-hoc scripts |

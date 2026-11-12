# Fleet Automation Orchestrator smoke service

`fleet_ao_smoke.yml` provides the visible state change used by the
`aap-demo` Fleet and Automation Orchestrator integration. It starts
`aap-demo-fleet-smoke.service` on the selected Linux host, then verifies that
the unit is active. The transient service sleeps for five minutes and systemd
collects it afterwards.

Product Demos setup creates a generic job template. The `aap-demo` integration
separately provisions its Fleet-scoped template, inventory, and Automation
Orchestrator workflow.

## Prerequisites

- Linux hosts with systemd and privilege to run `systemd-run`.
- For the generic template, hosts in **Ansible Product Demos Inventory** and SSH access through **APD Machine Credential**.

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Fleet AO Smoke Service | [`linux/fleet_ao_smoke.yml`](../fleet_ao_smoke.yml) | Starts and verifies the transient service on selected hosts |

The generic template requires a host pattern through its survey. Other job
templates must also provide `_hosts` to select their target hosts.

If a previous unit remains failed or uncollected, inspect it with
`systemctl status aap-demo-fleet-smoke.service` and clear the failed state with
`sudo systemctl reset-failed aap-demo-fleet-smoke.service` before retrying. If
the unit still exists, stop it with `sudo systemctl stop aap-demo-fleet-smoke.service`.

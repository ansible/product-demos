#!/usr/bin/env bash
set -euo pipefail

playbook=linux/fleet_ao_smoke.yml
test -f "$playbook"
rg -F 'systemd-run --collect --unit=aap-demo-fleet-smoke /usr/bin/sleep 300' "$playbook"
rg -F 'systemctl is-active --quiet aap-demo-fleet-smoke.service' "$playbook"

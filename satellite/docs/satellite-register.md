# Register with Satellite


Registers RHEL hosts with a Red Hat Satellite server. Uses the demo.satellite.register_host role to configure the Satellite URL, install the katello-ca-consumer package, and register the host.

## Prerequisites

- RHEL hosts in the <strong>Ansible Product Demos Inventory</strong>
- <strong>Satellite Collection</strong> credential configured
- Run <strong>APD | Single demo setup</strong> with <code>satellite</code>

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |
| Choose Environment | `env` | multiplechoice | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Register with Satellite | [`satellite/server_register.yml`](../server_register.yml) | Registers target RHEL hosts with the configured Satellite server |

## Related demos

| Demo | Description |
|------|-------------|
| 🛰️ [Compliance Scan with Satellite](./satellite-compliance-scan.md) | Run compliance scans on Satellite-managed hosts |
| 🐧 [Register with Insights](../../linux/docs/linux-register-insights.md) | Register directly with RHSM instead of through Satellite |

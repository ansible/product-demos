# Fact Scan


Scans hosts and gathers package and service facts. This populates the AAP fact cache with installed packages and running services, which can then be viewed in the host details page. Useful for inventory auditing and compliance checks.

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
| LINUX ǀ Fact Scan | [`linux/fact_scan.yml`](../fact_scan.yml) | Gathers package_facts and service_facts, caching them in AAP |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Troubleshoot](./linux-troubleshoot.md) | Active troubleshooting beyond passive fact gathering |
| 🚀 [Deploy Cloud Stack in AWS](../../cloud/docs/deploy-cloud-stack.md) | Deploy hosts to scan |

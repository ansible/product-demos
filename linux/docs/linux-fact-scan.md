---
layout: demo-detail
demo_slug: linux-fact-scan
---

Scans hosts and gathers package and service facts. This populates the AAP fact cache with installed packages and running services, which can then be viewed in the host details page. Useful for inventory auditing and compliance checks.

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
| LINUX | Fact Scan | [`linux/fact_scan.yml`](https://github.com/ansible/product-demos/blob/main/linux/fact_scan.yml) | Gathers package_facts and service_facts, caching them in AAP |

## Related demos

| Demo | Description |
|------|-------------|
| 🐧 [Troubleshoot](/product-demos/demos/linux-troubleshoot/) | Active troubleshooting beyond passive fact gathering |
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | Deploy hosts to scan |

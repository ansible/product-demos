---
layout: demo-detail
demo_slug: network-report
---

Generates an HTML network report by gathering facts from Cisco IOS, IOS-XR, and NX-OS devices. Collects interface, routing, and system information using the platform-specific facts modules and renders them into a browsable report.

## Prerequisites

- Network devices in inventory
- Network credentials configured
- A <code>reports</code> host for publishing the HTML report

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK | Report | [`network/report.yml`](https://github.com/ansible/product-demos/blob/main/network/report.yml) | Gathers facts from Cisco IOS, IOS-XR, and NX-OS devices and generates an HTML report |

## Related demos

| Demo | Description |
|------|-------------|
| 🌐 [Golden Configuration](/product-demos/demos/network-configuration/) | Apply configurations before generating a report |
| 🌐 [Backup](/product-demos/demos/network-backup/) | Back up configurations alongside reporting |

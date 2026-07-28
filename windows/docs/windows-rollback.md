---
layout: demo-detail
demo_slug: windows-rollback
---

A generic rollback playbook used as a cleanup step in Windows workflows. Outputs a configurable rollback message. Used by the Setup Active Directory Domain workflow as the failure handler to clean up resources on error.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong>

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| WINDOWS | Rollback | [`windows/rollback.yml`](https://github.com/ansible/product-demos/blob/main/windows/rollback.yml) | Outputs rollback message -- used as a failure handler in workflows |

## Related demos

| Demo | Description |
|------|-------------|
| 🪟 [Setup Active Directory Domain](/product-demos/demos/windows-setup-ad-domain/) | Uses this playbook as its failure cleanup handler |

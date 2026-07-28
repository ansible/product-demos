---
layout: demo-detail
demo_slug: network-backup
description: >-
  Backs up running configurations from network devices to a report server.
  Sets up a backup directory on the report server, then saves device configs.
  Provides a browsable backup archive via HTTP.
prerequisites:
  - "Network devices (routers) in inventory"
  - "A <code>reports</code> host for storing backups"
  - "Network credentials configured"
job_templates:
  - name: "NETWORK | Backup"
    playbook: network/backup.yml
    description: "Sets up a backup directory on the report server and saves device running configs"
related_demos:
  - slug: network-configuration
    description: "Apply configurations that you may want to back up first"
  - slug: network-report
    description: "Generate a report alongside backups"
---

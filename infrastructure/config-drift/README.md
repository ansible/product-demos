# Config drift detection and remediation (supporting files)

Playbooks, audit rules, Filebeat/Kafka configs, and EDA rulebooks for the **Event-Driven Configuration Drift Remediation** demo.

Documentation and validation steps: [`../docs/config-drift.md`](../docs/config-drift.md)

## Layout

| Path | Purpose |
|------|---------|
| [`auditd/sshd-config.rules`](auditd/sshd-config.rules) | Reference copy of the persistent audit rule |
| [`playbooks/deploy_audit_filebeat.yml`](playbooks/deploy_audit_filebeat.yml) | Deploy auditd (and later Filebeat) to RHEL hosts |
| [`filebeat/`](filebeat/) | Filebeat configuration (Stage 2) |
| [`kafka/`](kafka/) | Podman Compose Kafka stack (Stage 3) |
| [`collections/.../demo/config_drift`](../../collections/ansible_collections/demo/config_drift) | Ansible role implementation |

AAP job templates and workflows are defined in [`../setup.yml`](../setup.yml).

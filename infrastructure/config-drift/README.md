# Config drift detection and remediation (supporting files)

Playbooks, audit rules, Filebeat/Kafka configs, and EDA rulebooks for the **Event-Driven Configuration Drift Remediation** demo.

Documentation and validation steps: [`../docs/config-drift.md`](../docs/config-drift.md)

## Layout

| Path | Purpose |
|------|---------|
| [`auditd/sshd-config.rules`](auditd/sshd-config.rules) | Reference copy of the persistent audit rule |
| [`playbooks/deploy_audit_filebeat.yml`](playbooks/deploy_audit_filebeat.yml) | Deploy auditd (and later Filebeat) to RHEL hosts |
| [`playbooks/provision_kafka.yml`](playbooks/provision_kafka.yml) | Provision `aws_kafka` and deploy Podman Kafka |
| [`playbooks/setup_eda_activation.yml`](playbooks/setup_eda_activation.yml) | Create EDA rulebook activation for Kafka events |
| [`playbooks/check_cloud_stack.yml`](playbooks/check_cloud_stack.yml) | Verify aws_rhel8/aws_rhel9 before full setup workflow |
| [`playbooks/drift_sshd.yml`](playbooks/drift_sshd.yml) | Introduce `PermitRootLogin yes` drift for demo |
| [`playbooks/remediate_sshd.yml`](playbooks/remediate_sshd.yml) | Restore `sshd_config` after drift |
| [`filebeat/`](filebeat/) | Filebeat configuration (Stage 2) |
| [`kafka/`](kafka/) | Podman Kafka stack (Stage 3) |
| [`../../extensions/eda/rulebooks/`](../../extensions/eda/rulebooks/) | EDA rulebooks (Stage 4) |
| [`collections/.../demo/config_drift`](../../collections/ansible_collections/demo/config_drift) | Ansible role implementation |

AAP job templates and workflows are defined in [`../setup.yml`](../setup.yml).

# demo.config_drift

Ansible collection supporting the **Infrastructure | Config Drift Remediation** demo
  (`infrastructure/config-drift/`).

## Roles

| Role | Purpose |
|------|---------|
| `audit_filebeat` | Persistent auditd rules for `/etc/ssh/sshd_config` and Filebeat (console or Kafka output) |
| `kafka_queue` | Single-node Podman KRaft Kafka broker and `linux-audit-events` topic |

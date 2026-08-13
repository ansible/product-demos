# Event-Driven Configuration Drift Remediation with Ansible Automation Platform

Production-style demo: a Linux administrator manually changes a protected configuration file, Linux auditing detects the change, Filebeat ships the event to Kafka, Event-Driven Ansible evaluates the signal, and AAP restores the approved configuration.

```text
manual configuration change
  → Linux audit event (auditd)
  → Filebeat
  → Kafka
  → Event-Driven Ansible
  → AAP remediation
```

Ansible is not polling every server for drift. The infrastructure generates a signal when something changes; Event-Driven Ansible decides whether to act; AAP runs the approved remediation playbook.

## Architecture

```text
Linux Server (aws_rhel9)
   │
   │  manual config change (e.g. vi /etc/ssh/sshd_config)
   ▼
auditd  (-w /etc/ssh/sshd_config -p wa -k sshd_config_change)
   │
   ▼
Filebeat (auditd module)          [Stage 2]
   │
   ▼
Kafka (dedicated EC2, Podman)    [Stage 3]
   │
   ▼
Event-Driven Ansible rulebook      [Stage 4]
   │
   ▼
AAP Job Template                   [Stage 5]
   │
   ▼
Ansible restores desired sshd_config
```

## Prerequisites

- **Deploy Cloud Stack in AWS** — provides `aws_rhel8`, `aws_rhel9`, and other targets
- **APD | Single demo setup** — choose `event-driven-config-drift` (or include in multi-demo setup)
- **Automation Decisions (EDA)** enabled on your AAP instance (for Stages 4–5)
- SSH access via **APD Machine Credential**

## Repository layout

| Path | Purpose |
|------|---------|
| [`auditd/sshd-config.rules`](auditd/sshd-config.rules) | Reference copy of the persistent audit rule |
| [`playbooks/deploy_audit_filebeat.yml`](playbooks/deploy_audit_filebeat.yml) | Deploy auditd (and later Filebeat) to RHEL hosts |
| [`collections/.../demo/config_drift`](collections/ansible_collections/demo/config_drift) | Ansible role implementation |
| [`setup.yml`](setup.yml) | AAP job templates and workflows |
| [`docs/demo-flow.md`](docs/demo-flow.md) | Stage-by-stage validation and live demo script |

## Build status

| Stage | Component | Status |
|-------|-----------|--------|
| 1 | auditd persistent watch on `/etc/ssh/sshd_config` | **Implemented** |
| 2 | Filebeat auditd module (console debug) | Planned |
| 3 | Kafka on dedicated AWS EC2 (Podman KRaft) | Planned |
| 4 | EDA rulebook + activation | Planned |
| 5 | AAP sshd remediation playbook | Planned |

## Quick start — Stage 1

1. Run **APD | Single demo setup** with demo category `event-driven-config-drift`.
2. Run **LINUX | Config Drift - Deploy Audit and Filebeat** against `aws_rhel9` (leave **Deploy Filebeat** = false).
3. SSH to the host and validate — see [`docs/demo-flow.md`](docs/demo-flow.md).

## AAP job templates

| Template | Stage |
|----------|-------|
| LINUX ǀ Config Drift - Deploy Audit and Filebeat | 1–2 |
| Infrastructure ǀ AWS - Provision Kafka Queue | 3 |
| Infrastructure ǀ Setup Rulebook for Kafka Queue - Config Drift & Remediation | 4 |
| LINUX ǀ SSHD Configuration Remediation | 5 |
| Infrastructure ǀ Setup Configuration Drift Detection & Remediation with EDA | Setup workflow |

## Production positioning

In production, Kafka might be replaced by an enterprise event bus or SIEM forwarding path. The pattern stays the same: **detect at the source → route events → decide in EDA → remediate in AAP**.

## Branch

Development branch: `feature/event-driven-config-drift`. Point the **Ansible Product Demos** project SCM branch here while testing.

# Event-Driven Configuration Drift Remediation

Production-style demo: a Linux administrator manually changes a protected configuration file, Linux auditing detects the change, Filebeat ships the event to Kafka, Event-Driven Ansible evaluates the signal, and AAP restores the approved configuration.

```text
manual configuration change
  → Linux audit event (auditd)
  → Filebeat
  → Kafka
  → Event-Driven Ansible
  → AAP remediation
```

## Prerequisites

- **Deploy Cloud Stack in AWS** — `aws_rhel9` (or similar) in inventory
- **APD | Single demo setup** — category `infrastructure` or `linux`
- **RHSM Registration** credential — org ID and activation key (see **LINUX | Register RHEL with RHSM**)
- **Automation Decisions (EDA)** on AAP (Stages 4–5)
- SSH access via **APD Machine Credential**

Recommended order after cloud stack deploy:

1. **LINUX | Register RHEL with RHSM** — default `_hosts`: `aws_rhel*`
2. **LINUX | Config Drift - Deploy Audit and Filebeat** — default `_hosts`: `aws_rhel*`

### Host targeting

| Pattern | Hosts matched | Use when |
|---------|---------------|----------|
| `aws_rhel9` | One RHEL 9 worker | Quick single-host demo |
| `aws_rhel*` | `aws_rhel8` + `aws_rhel9` | Filebeat/auditd on every RHEL **worker** VM |
| `reports` | Report server only | Not a config-drift target — different role in the stack |

`aws_rhel*` does **not** match `reports`. If your job run includes `reports`, you used a broader limit than `aws_rhel*` (for example a group or `*`).

Unreachable hosts are skipped (`ignore_unreachable`) so one bad SSH target does not block the rest of the fleet.

## Job templates

| Template | Playbook | Stage |
|----------|----------|-------|
| LINUX ǀ Config Drift - Deploy Audit and Filebeat | [`infrastructure/config-drift/playbooks/deploy_audit_filebeat.yml`](../config-drift/playbooks/deploy_audit_filebeat.yml) | 1–2, 3 (kafka output) |
| Infrastructure ǀ AWS - Provision Kafka Queue | [`infrastructure/config-drift/playbooks/provision_kafka.yml`](../config-drift/playbooks/provision_kafka.yml) | 3 |
| Infrastructure ǀ Setup Rulebook for Kafka Queue - Config Drift & Remediation | [`infrastructure/config-drift/playbooks/setup_eda_activation.yml`](../config-drift/playbooks/setup_eda_activation.yml) | 4 |
| LINUX ǀ SSHD Configuration Remediation | [`infrastructure/config-drift/playbooks/remediate_sshd.yml`](../config-drift/playbooks/remediate_sshd.yml) | 4–5 |

## Build status

| Stage | Component | Status |
|-------|-----------|--------|
| 1 | auditd persistent watch on `/etc/ssh/sshd_config` | **Implemented** |
| 2 | Filebeat auditd module (console or Kafka output) | **Implemented** |
| 3 | Kafka on dedicated AWS EC2 (Podman KRaft) | **Implemented** — [walkthrough](config-drift-kafka.md) |
| 4 | EDA rulebook + activation | **Implemented** — [walkthrough](config-drift-eda.md) |
| 5 | AAP sshd remediation playbook | **Implemented** (basic PermitRootLogin restore) |

---

## Stage 1 — auditd

### Setup

1. Run **APD | Single demo setup** with `infrastructure`.
2. Run **LINUX | Config Drift - Deploy Audit and Filebeat** — default `_hosts`: `aws_rhel*`.

### What was deployed

Persistent rule in `/etc/audit/rules.d/99-sshd-config.rules`:

```text
-w /etc/ssh/sshd_config -p wa -k sshd_config_change
```

| Flag | Meaning |
|------|---------|
| `-w` | Watch this path |
| `-p wa` | Writes and attribute changes |
| `-k sshd_config_change` | Searchable audit key |

### Verify rule is loaded

```bash
sudo auditctl -l | grep sshd_config
```

### Trigger a test change

```bash
sudo cp -a /etc/ssh/sshd_config /tmp/sshd_config.bak
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
grep PermitRootLogin /etc/ssh/sshd_config
```

### Inspect audit events

```bash
sudo ausearch -k sshd_config_change -ts recent
```

### Understanding the audit records

One file edit typically produces **multiple correlated records**:

| Record type | What it tells you |
|-------------|-------------------|
| `type=SYSCALL` | Syscall that performed the write |
| `type=PATH` | File path — look for `name="/etc/ssh/sshd_config"` |
| `type=PROCTITLE` | Command line (e.g. `sed`, `vi`) |
| `key=sshd_config_change` | Matches our `-k` tag |
| `uid` / `auid` | Effective user / login UID |
| `comm` / `exe` | Process name and executable path |

### Restore after testing

```bash
sudo cp -a /tmp/sshd_config.bak /etc/ssh/sshd_config
```

---

## Stage 2 — Filebeat

Filebeat is installed and configured automatically by the same job template.

- Elastic 8.x `filebeat` package with the **auditd** module
- Reads `/var/log/audit/audit.log*`
- **Console output** (pretty JSON) for validation before Kafka is wired in Stage 3

### Verify Filebeat is running

```bash
sudo systemctl status filebeat
sudo journalctl -u filebeat -f
```

### Trigger a test change and watch events

```bash
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
```

In another session on the host:

```bash
sudo journalctl -u filebeat -f
```

You should see parsed JSON with audit fields, hostname, and `@timestamp`.

Foreground debug:

```bash
sudo systemctl stop filebeat
sudo filebeat -e -c /etc/filebeat/filebeat.yml
```

## Stage 3 — Kafka

Full step-by-step walkthrough: **[Config Drift — Kafka Queue](config-drift-kafka.md)** (provision broker, wire Filebeat, consume and validate `sshd_config_change` events).

### Quick reference

1. Run **Infrastructure | AWS - Provision Kafka Queue** (same region/owner as cloud stack).
2. Sync **AWS Inventory** so `aws_kafka` appears.
3. Re-run **LINUX | Config Drift - Deploy Audit and Filebeat** with **Filebeat output**: `kafka`.
4. On `aws_kafka`, consume topic `linux-audit-events` and filter for `sshd_config_change` (see kafka walkthrough for `9094` admin listener).

## Stage 4 — Event-Driven Ansible

Full walkthrough: **[Config Drift — EDA](config-drift-eda.md)**.

1. Sync the **Ansible Product Demos** EDA project.
2. Run **Infrastructure | Setup Rulebook for Kafka Queue - Config Drift & Remediation**.
3. Confirm activation **config_drift_kafka** is running.
4. Drift `sshd_config` on a worker — **LINUX | SSHD Configuration Remediation** should launch automatically.

## Stage 5 — AAP remediation

**LINUX | SSHD Configuration Remediation** restores `PermitRootLogin no`, validates with `sshd -t`, and reloads `sshd`. It resolves the target host from `config_drift_target_ip` (private IP passed by the EDA rulebook).

## Why it matters

- Demonstrates a credible production pattern: audit at the OS, ship via a log agent, route through Kafka, decide in EDA, remediate in AAP
- Ansible is not polling for drift — infrastructure emits a signal when configuration changes
- Maps to enterprise deployments where Kafka may be replaced by a SIEM or cloud event bus

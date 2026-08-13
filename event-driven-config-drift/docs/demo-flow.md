# Demo flow — Event-Driven Configuration Drift Remediation

Incremental validation guide. Complete each stage before moving to the next.

## Prerequisites

1. **Deploy Cloud Stack in AWS** — `aws_rhel9` (or similar) in inventory
2. **APD | Single demo setup** — category `event-driven-config-drift`
3. **LINUX | Config Drift - Deploy Audit and Filebeat** — `_hosts`: `aws_rhel9`, **Deploy Filebeat**: `false`

---

## Stage 1 — auditd

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

Expected output includes:

```text
-w /etc/ssh/sshd_config -p wa -k sshd_config_change
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
| `type=SYSCALL` | Syscall that performed the write (`syscall=open` / `write`, etc.) |
| `type=PATH` | File path — look for `name="/etc/ssh/sshd_config"` |
| `type=CWD` | Working directory of the process |
| `type=PROCTITLE` | Command line (e.g. `sed`, `vi`) |
| `key=sshd_config_change` | Matches our `-k` tag |
| `uid` | Effective user ID of the process |
| `auid` | Login UID (`4294967295` = not attributable to a login session) |
| `comm` / `exe` | Short process name and executable path |

### Restore after testing

```bash
sudo cp -a /tmp/sshd_config.bak /etc/ssh/sshd_config
```

---

## Stage 2 — Filebeat (not yet on this branch)

*Coming next: Filebeat auditd module, foreground debug with `filebeat -e`.*

---

## Stage 3 — Kafka (not yet on this branch)

*Coming next: dedicated EC2 + Podman KRaft, topic `linux-audit-events`.*

---

## Stage 4 — Event-Driven Ansible (not yet on this branch)

*Coming next: rulebook under `extensions/eda/rulebooks/` after inspecting real Kafka JSON.*

---

## Stage 5 — AAP remediation (not yet on this branch)

*Coming next: `LINUX | SSHD Configuration Remediation` with `sshd -t` validation.*

---

## Live demo (full pipeline — future)

| Terminal | Action |
|----------|--------|
| 1 | `kafka-console-consumer` on `linux-audit-events` |
| 2 | EDA activation / Automation Decisions logs |
| 3 | SSH to RHEL host — drift `sshd_config`, wait, verify restoration |

# Config Drift — Event-Driven Ansible (Stage 4)

Activate a rulebook that subscribes to Kafka topic `linux-audit-events`, filters for `sshd_config_change` audit events, and launches **LINUX | SSHD Configuration Remediation**.

## Prerequisites

| Step | Demo page |
|------|-----------|
| Stages 1–2 — auditd + Filebeat | [Config Drift Remediation](config-drift.md) |
| Stage 3 — Kafka broker + Filebeat output `kafka` | [Config Drift — Kafka Queue](config-drift-kafka.md) |
| EDA enabled on your AAP instance | Automation Decisions in the UI |
| EDA project synced | **Ansible Product Demos** (same SCM project as Controller) |

## What the rulebook does

```text
Kafka topic linux-audit-events
  → filter: message contains sshd_config_change and type=SYSCALL
  → throttle: once per host IP per 60 seconds
  → run_job_template: LINUX | SSHD Configuration Remediation
      extra_vars.config_drift_target_ip = event.host.ip[0]
```

Rulebook file: [`extensions/eda/rulebooks/config_drift_kafka.yml`](../../extensions/eda/rulebooks/config_drift_kafka.yml)

## Step 1 — Sync the EDA project

The setup job creates the **Ansible Product Demos** EDA project automatically (mirroring the Controller project's SCM URL and branch) and syncs it. You do not need to create the EDA project manually.

If you prefer to verify first:

1. In AAP, open **Automation Decisions → Projects**.
2. Confirm **Ansible Product Demos** exists and contains `extensions/eda/rulebooks/config_drift_kafka.yml`.

## Step 2 — Activate the rulebook

1. Run **APD | Single demo setup** with category `infrastructure` (creates job templates).
2. Run **Infrastructure | Setup Rulebook for Kafka Queue - Config Drift & Remediation**.

The setup job reads `aws_kafka` from inventory and creates (or updates) EDA activation `config_drift_kafka` with broker host, topic, and rulebook path.

| Activation setting | Source |
|--------------------|--------|
| `config_drift_kafka_broker_host` | `aws_kafka` private IP from inventory |
| `config_drift_kafka_topic` | `linux-audit-events` |
| Decision environment | Product Demos EE |

## Step 3 — Verify activation is running

1. **Automation Decisions → Rulebook activations**
2. Open **config_drift_kafka** — status should be **Running**
3. Check activation logs for Kafka consumer connection to `PRIVATE_IP:9092`

## Step 4 — End-to-end test

1. On a worker, drift `sshd_config`:

   ```bash
   sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
   grep PermitRootLogin /etc/ssh/sshd_config
   ```

2. Watch **Automation Decisions** activation logs — a matching event should appear within seconds.

3. Watch **Automation Execution** — **LINUX | SSHD Configuration Remediation** should launch with `config_drift_target_ip` set to the worker private IP.

4. Confirm remediation on the worker:

   ```bash
   grep PermitRootLogin /etc/ssh/sshd_config
   ```

   Expected: `PermitRootLogin no`

## Event shape EDA matches on

Filebeat publishes JSON like:

```json
{
  "message": "type=SYSCALL ... key=\"sshd_config_change\" ... SYSCALL=rename ...",
  "host": { "ip": ["10.0.1.244"], "hostname": "ip-10-0-1-244..." }
}
```

The rulebook condition requires both `sshd_config_change` and `type=SYSCALL` to ignore unrelated audit noise and reduce duplicate firings from companion records (`PATH`, `PROCTITLE`).

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Activation won't start | EDA project synced; decision environment **Product Demos EE** exists |
| No events in activation log | Filebeat output is `kafka`; consumer on broker shows `sshd_config_change` events |
| Job not launched | Activation enabled; rulebook condition matches your test event |
| Remediation job fails host lookup | Sync AWS inventory; worker `private_ip_address` must match `event.host.ip[0]` |
| Job runs but sshd unchanged | Check remediation job stdout; `sshd -t` must pass before reload |

## Next step

Stage 5 hardening (additional sshd settings, notifications, workflow chaining) builds on **LINUX | SSHD Configuration Remediation**. See [Config Drift Remediation](config-drift.md) for the full pipeline overview.

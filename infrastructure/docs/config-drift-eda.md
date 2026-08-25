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
  → filter: event.body.message contains sshd_config_change and type=SYSCALL
  → throttle: once per host IP per 15 seconds
  → run_job_template: LINUX | SSHD Configuration Remediation
      config_drift_target_ip from event.body.host.ip[0]
```

Rulebook file: [`extensions/eda/rulebooks/config_drift_kafka.yml`](../../extensions/eda/rulebooks/config_drift_kafka.yml)

## Step 1 — Sync the EDA project

The setup job creates the **Ansible Product Demos** EDA project automatically (mirroring the Controller project's SCM URL and branch) and syncs it. You do not need to create the EDA project manually.

If you prefer to verify first:

1. In AAP, open **Automation Decisions → Projects**.
2. Confirm **Ansible Product Demos** exists and contains `extensions/eda/rulebooks/config_drift_kafka.yml`.

## Step 2 — Activate the rulebook

1. Run **APD | Single demo setup** with category `infrastructure` (creates job templates).
2. Run **Infrastructure | Config Drift - Full Setup** (recommended), or **Infrastructure | Setup Rulebook for Kafka Queue - Config Drift & Remediation** alone.

The setup job reads `aws_kafka` from inventory and creates (or updates) EDA activation `config_drift_kafka` with broker host, topic, and rulebook path.

| Activation setting | Source |
|--------------------|--------|
| `config_drift_kafka_broker_host` | `aws_kafka` public IP from inventory |
| `config_drift_kafka_broker_port` | `9095` (external listener for EDA) |
| `config_drift_kafka_topic` | `linux-audit-events` |
| Decision environment | **Product Demos DE** (`de-minimal-rhel9`, includes `ansible-rulebook`) |

## Step 3 — Verify activation is running

1. **Automation Decisions → Rulebook activations**
2. Open **config_drift_kafka** — status should be **Running**
3. Check activation logs for Kafka consumer connection to `PUBLIC_IP:9095` (external listener)

## Step 4 — End-to-end test

**From AAP (recommended):** run **LINUX | Config Drift - Introduce SSHD Drift** with default limit `aws_rhel*`.

**Or manually** on a worker, drift `sshd_config`:

```bash
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
grep PermitRootLogin /etc/ssh/sshd_config
```

1. Watch **Automation Decisions** activation logs — a matching event should appear within seconds.
2. Watch **Automation Execution** — **LINUX | SSHD Configuration Remediation** should launch with `config_drift_target_ip` set to the worker private IP.
3. Confirm remediation on the worker:

   ```bash
   grep PermitRootLogin /etc/ssh/sshd_config
   ```

   Expected: `PermitRootLogin no`

## Event shape EDA matches on

The rulebook reads Filebeat JSON from `event.body`. The `message` field contains the raw audit line; `host.ip[0]` is the worker private IP passed to remediation.

```json
{
  "body": {
    "message": "type=SYSCALL ... key=\"sshd_config_change\" ... SYSCALL=rename ...",
    "host": { "ip": ["10.0.1.244"], "hostname": "ip-10-0-1-244..." }
  }
}
```

The rulebook condition requires both `sshd_config_change` and `type=SYSCALL` to ignore unrelated audit noise and reduce duplicate firings from companion records (`PATH`, `PROCTITLE`).

## Troubleshooting

| Symptom | Check |
|---------|-------|
| Activation won't start | EDA project synced; decision environment **Product Demos DE** uses `de-minimal-rhel9` (not the Controller EE) |
| Activation Failed, 0 rules | Decision environment must include `ansible-rulebook`; Controller EEs such as Product Demos EE will not work |
| `404` on `/api/v2/config/` in activation log | EDA AAP credential host must include `/api/controller` on AAP 2.7 gateway deployments |
| No events in activation log | Filebeat output is `kafka`; consumer on broker shows `sshd_config_change` events |
| `KafkaConnectionError` on private IP | Re-run Kafka provision for external listener; EDA must use public IP `:9095` |
| Job not launched | Activation enabled; rulebook condition matches your test event |
| Remediation job fails host lookup | Sync AWS inventory; worker `private_ip_address` must match `event.body.host.ip[0]` |
| Job runs but sshd unchanged | Check remediation job stdout; `sshd -t` must pass before reload |

## Next step

Stage 5 hardening (additional sshd settings, notifications, workflow chaining) builds on **LINUX | SSHD Configuration Remediation**. See [Config Drift Remediation](config-drift.md) for the full pipeline overview.

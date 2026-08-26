# Config Drift — Kafka Queue (Stage 3)

Wire Filebeat audit events from your RHEL workers into a dedicated `aws_kafka` broker so Event-Driven Ansible can react to `sshd_config` changes without polling.

```text
/etc/ssh/sshd_config change
  → auditd (key: sshd_config_change)
  → Filebeat auditd module
  → Kafka topic linux-audit-events
  → (Stage 4) EDA rulebook
  → (Stage 5) AAP remediation
```

## Prerequisites

| Step | Job template | Notes |
|------|--------------|-------|
| Cloud stack | **Deploy Cloud Stack in AWS** | `aws_rhel8`, `aws_rhel9`, VPC `10.0.0.0/16` |
| Stage 1–2 | **LINUX \| Config Drift - Deploy Audit and Filebeat** | `_hosts`: `aws_rhel*`, Filebeat output: `console` |
| AAP setup | **APD \| Single demo setup** | category `infrastructure` |

## Architecture

| Component | Value |
|-----------|-------|
| EC2 host | `aws_kafka` (RHEL 9, `t3.medium`) |
| Broker image | `docker.io/apache/kafka:3.9.0` (Podman KRaft) |
| Worker-facing listener | `PRIVATE_IP:9092` (`PLAINTEXT`) |
| EDA-facing listener | `PUBLIC_IP:9095` (`EXTERNAL`) |
| Local admin listener | `127.0.0.1:9094` (`PLAINTEXT_LOCAL`) |
| Topic | `linux-audit-events` |
| Provision job | **Infrastructure \| AWS - Provision Kafka Queue** |
| Filebeat job | **LINUX \| Config Drift - Deploy Audit and Filebeat** (output: `kafka`) |

Workers ship to the broker **private IP** on port `9092`. EDA rulebook activations on AAP use the broker **public IP** on port `9095` because activation pods run outside the demo VPC. Admin commands on the broker host use `127.0.0.1:9094`.

## Step 1 — Provision the broker

1. Run **Infrastructure \| AWS - Provision Kafka Queue**.
2. Survey: same **region** and **owner** tag as your cloud stack (`aws-test-key`, `aws-test-sg`, and `aws-test-subnet` are applied automatically).
3. Wait for the job to finish both plays:
   - Provision `aws_kafka` EC2 (or reuse existing)
   - Deploy Podman Kafka and create topic `linux-audit-events`

## Step 2 — Sync inventory

Sync **AWS Inventory** so `aws_kafka` appears in **Ansible Product Demos Inventory** with its private IP.

The Filebeat playbook resolves the broker as `hostvars['aws_kafka']` → `private_ip_address:9092`.

## Step 3 — Point Filebeat at Kafka

Re-run **LINUX \| Config Drift - Deploy Audit and Filebeat**:

| Survey field | Value |
|--------------|-------|
| `_hosts` | `aws_rhel*` |
| **Filebeat output** | `kafka` |

This rewrites `/etc/filebeat/filebeat.yml` on each worker to publish to `aws_kafka:9092`. Auditd rules are unchanged.

## Step 4 — Watch events (presenter dashboard)

After **Infrastructure \| AWS - Provision Kafka Queue**, open the live dashboard on the broker public IP:

```text
http://PUBLIC_IP/
```

The page auto-refreshes every few seconds. When someone edits `/etc/ssh/sshd_config` on a worker, you should see a green line like:

```text
/etc/ssh/sshd_config modified on 10.0.1.244 — event published
```

That is the same filter the EDA rulebook uses (`sshd_config_change` + `type=SYSCALL`). Open AAP next and confirm remediation fired.

### Manual consumer (optional)

SSH to `aws_kafka` if you prefer the raw Kafka stream.

Start a consumer on the **local admin listener** (`9094`):

```bash
sudo podman run --rm --network container:kafka docker.io/apache/kafka:3.9.0 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server 127.0.0.1:9094 \
  --topic linux-audit-events \
  --from-beginning
```

You will see a stream of JSON lines — mostly background audit noise (`CRYPTO_SESSION`, `USER_LOGIN`, PAM events). That is normal; Filebeat ships the full `/var/log/audit/audit.log`.

Filter for drift events:

```bash
sudo podman run --rm --network container:kafka docker.io/apache/kafka:3.9.0 \
  /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server 127.0.0.1:9094 \
  --topic linux-audit-events \
  --from-beginning | grep sshd_config_change
```

## Step 5 — Trigger a config drift event

On a RHEL worker (`aws_rhel8` or `aws_rhel9`), edit the protected file:

```bash
sudo vi /etc/ssh/sshd_config
# change PermitRootLogin, save and quit
```

Or non-interactively:

```bash
sudo sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
```

## What to look for

A single `vi` save produces **several** Kafka messages — one per audit syscall. That is expected. Look for lines where `message` contains `key="sshd_config_change"`.

Example fields from a real drift event:

```json
{
  "@timestamp": "2026-08-25T14:21:28.956Z",
  "message": "type=SYSCALL ... comm=\"vi\" ... key=\"sshd_config_change\" ... SYSCALL=rename AUID=\"ec2-user\" ...",
  "host": {
    "hostname": "ip-10-0-1-244.us-east-2.compute.internal",
    "ip": ["10.0.1.244", "fe80::..."],
    "os": { "platform": "rhel", "version": "9.6 (Plow)" }
  },
  "event": { "module": "auditd", "dataset": "auditd.log" }
}
```

| Field | Demo meaning |
|-------|--------------|
| `key="sshd_config_change"` | Matches our auditd watch on `/etc/ssh/sshd_config` |
| `comm="vi"` / `SYSCALL=rename` | Typical atomic save (temp file → `sshd_config`) |
| `AUID="ec2-user"` | Login user who made the change |
| `host.ip[0]` | Worker private IP — used in Stage 4 to pick the remediation target |
| `host.hostname` | EC2 internal DNS name (not the inventory name `aws_rhel9`) |

## How this connects to sshd_config

Stage 1 deployed a persistent audit rule:

```text
-w /etc/ssh/sshd_config -p wa -k sshd_config_change
```

| Flag | Meaning |
|------|---------|
| `-w` | Watch this path |
| `-p wa` | Writes and attribute changes |
| `-k sshd_config_change` | Searchable key in audit and Kafka `message` |

Filebeat does **not** filter at the source — it ships all audit events. Stage 4 (EDA) filters on `sshd_config_change` in the rulebook condition.

## Troubleshooting

| Symptom | Check |
|---------|-------|
| No `aws_kafka` in inventory | Sync **AWS Inventory** after provision |
| Filebeat job fails on Kafka | Confirm `aws_kafka` in inventory; re-run provision |
| Consumer shows noise only | Run the `grep sshd_config_change` filter; then edit `sshd_config` |
| `podman ps` empty as `ec2-user` | Broker runs in **root** podman — use `sudo podman ps` |
| Broker crash-loop | `sudo podman logs kafka` — listener config must use `CONTROLLER://127.0.0.1:9093` |
| EDA cannot connect after redeploying cloud stack | **Deploy Cloud Stack in AWS** manages `aws-test-sg` and now keeps TCP **9095** open for EDA. On older revisions, re-run **Infrastructure \| AWS - Provision Kafka Queue** to re-add the rule, or add TCP 9095 inbound on `aws-test-sg` manually. Verify with `nc -zv PUBLIC_IP 9095` from outside the VPC. |

### Security group and idempotent cloud deploy

Kafka and the cloud stack share **`aws-test-sg`**. **Cloud \| AWS \| Create VPC** (`cloud/create_vpc.yml`) defines the full inbound rule set for that group. Port **9095** is included so EDA can reach the Kafka **EXTERNAL** listener after you re-run **Deploy Cloud Stack in AWS** for an idempotency demo.

If you provisioned Kafka before this rule was in Create VPC, one **Provision Kafka Queue** run still adds 9095 with `purge_rules: false`. After that, Create VPC and Kafka provision agree on the same SG.

## Next step

[Config Drift — EDA rulebook (Stage 4)](config-drift-eda.md): activate the rulebook that listens on `linux-audit-events` and launches remediation.

## Related demos

| Demo | Stage |
|------|-------|
| [Config Drift Remediation](config-drift.md) | Full pipeline overview |
| [Config Drift — EDA](config-drift-eda.md) | Stage 4 |

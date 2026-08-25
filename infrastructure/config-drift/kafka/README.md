# Stage 3 — Kafka (Podman KRaft)

Single-node Apache Kafka 3.9 in Podman on a dedicated `aws_kafka` EC2 instance.

| Item | Value |
|------|-------|
| Image | `docker.io/apache/kafka:3.9.0` |
| Topic | `linux-audit-events` |
| Broker port | `9092` (VPC-internal) |
| Provision job | **Infrastructure \| AWS - Provision Kafka Queue** |

`compose.yml` documents the container environment. The `demo.config_drift.kafka_queue` role applies the same settings with `containers.podman.podman_container`.

After provisioning, sync **AWS Inventory** and re-run **LINUX \| Config Drift - Deploy Audit and Filebeat** with Filebeat output `kafka`.

# Troubleshoot Containerlab


Runs read-only diagnostics on the containerlab hypervisor through AAP using the **Containerlab SSH** credential. Use this when day-2 jobs such as Backup or Report fail and you cannot export the hypervisor private key from AAP.

## Prerequisites

- Containerlab hypervisor provisioned via **NETWORK ǀ Deploy Containerlab Stack**
- **AWS** credential configured for EC2 discovery
- **Containerlab SSH** credential populated during hypervisor provisioning

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| AWS Region | `clab_aws_region` | multiplechoice | Yes |

Options: `us-east-2` (default), `us-west-2`.

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ Containerlab ǀ Troubleshoot | [`network/troubleshoot_containerlab.yml`](../troubleshoot_containerlab.yml) | Discovers the hypervisor, probes device ports, and collects containerlab and podman status |

## What it checks

1. **Hypervisor discovery** — Finds the running EC2 instance tagged `deployment=containerlab`
2. **External port probes** — Tests TCP connectivity to ports 22, 2122, and 2123 from the execution node
3. **Hypervisor health** — Uptime, memory, and disk usage on the image volume
4. **containerlab status** — `containerlab version` and `containerlab inspect`
5. **Podman containers** — Lists containers for both `ec2-user` and root runtimes
6. **Local device SSH probes** — Checks whether n9kv and cat8kv respond on 2122 and 2123 on the hypervisor
7. **Recent container logs** — Last 20 log lines for n9kv and cat8kv containers when inspect succeeds

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Containerlab Stack](./network-deploy-containerlab-stack.md) | Redeploy the topology if containers are down |
| 🌐 [Backup](./network-backup.md) | Retry after troubleshooting shows device ports are open |
| 🌐 [Report](./network-report.md) | Verify device connectivity after fixing the lab |

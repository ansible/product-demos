# AWS — Transit Networking


Creates a hub-and-spoke network topology using AWS Transit Gateway. Provisions multiple VPCs connected through a central transit gateway, with DMZ and private network zones. Includes bastion host configuration for cross-VPC SSH access.

## Prerequisites

- AWS credential configured
- SSH keypair for DMZ and private network hosts

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Create Transit Infrastructure | [`cloud/create_transit_network.yml`](../create_transit_network.yml) | Provisions VPCs, transit gateway, attachments, and configures bastion SSH access |

## Related demos

| Demo | Description |
|------|-------------|
| ☁️ [AWS — Peer Networking](./cloud-peer-networking.md) | Alternative direct-peering topology for simpler two-VPC setups |
| ☁️ [AWS — Create VPC](./cloud-create-vpc.md) | Standalone VPC creation for simpler setups |

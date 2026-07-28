---
layout: demo-detail
demo_slug: cloud-transit-networking
---

Creates a hub-and-spoke network topology using AWS Transit Gateway. Provisions multiple VPCs connected through a central transit gateway, with DMZ and private network zones. Includes bastion host configuration for cross-VPC SSH access.

## Prerequisites

- AWS credential configured
- SSH keypair for DMZ and private network hosts

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud | AWS | Create Transit Infrastructure | [`cloud/create_transit_network.yml`](https://github.com/ansible/product-demos/blob/main/cloud/create_transit_network.yml) | Provisions VPCs, transit gateway, attachments, and configures bastion SSH access |

## Related demos

| Demo | Description |
|------|-------------|
| ☁️ [AWS — Peer Networking](/product-demos/demos/cloud-peer-networking/) | Alternative direct-peering topology for simpler two-VPC setups |
| ☁️ [AWS — Create VPC](/product-demos/demos/cloud-create-vpc/) | Standalone VPC creation for simpler setups |

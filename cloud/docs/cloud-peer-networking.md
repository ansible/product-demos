# AWS — Peer Networking


Creates a multi-VPC peered network topology with a DMZ and private network. Provisions VPCs, subnets, peering connections, route tables, and EC2 instances in each zone. Configures SSH bastion access from DMZ hosts to private network hosts.

## Prerequisites

- AWS credential configured
- SSH keypair for DMZ and private network hosts

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Create Peer Infrastructure | [`cloud/create_peer_network.yml`](https://github.com/ansible/product-demos/blob/main/cloud/create_peer_network.yml) | Provisions peered VPCs, subnets, instances, and configures SSH bastion access |

## Related demos

| Demo | Description |
|------|-------------|
| ☁️ [AWS — Transit Networking](/product-demos/demos/cloud-transit-networking/) | Alternative hub-and-spoke topology using transit gateways |
| ☁️ [AWS — Create VPC](/product-demos/demos/cloud-create-vpc/) | Standalone VPC creation for simpler setups |

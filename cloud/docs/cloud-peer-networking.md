---
layout: demo-detail
demo_slug: cloud-peer-networking
description: >-
  Creates a multi-VPC peered network topology with a DMZ and private network.
  Provisions VPCs, subnets, peering connections, route tables, and EC2
  instances in each zone. Configures SSH bastion access from DMZ hosts to
  private network hosts.
prerequisites:
  - "AWS credential configured"
  - "SSH keypair for DMZ and private network hosts"
job_templates:
  - name: "Cloud | AWS | Create Peer Infrastructure"
    playbook: cloud/create_peer_network.yml
    description: "Provisions peered VPCs, subnets, instances, and configures SSH bastion access"
related_demos:
  - slug: cloud-transit-networking
    description: "Alternative hub-and-spoke topology using transit gateways"
  - slug: cloud-create-vpc
    description: "Standalone VPC creation for simpler setups"
---

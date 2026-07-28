---
layout: demo-detail
demo_slug: cloud-transit-networking
description: >-
  Creates a hub-and-spoke network topology using AWS Transit Gateway.
  Provisions multiple VPCs connected through a central transit gateway, with
  DMZ and private network zones. Includes bastion host configuration for
  cross-VPC SSH access.
prerequisites:
  - "AWS credential configured"
  - "SSH keypair for DMZ and private network hosts"
job_templates:
  - name: "Cloud | AWS | Create Transit Infrastructure"
    playbook: cloud/create_transit_network.yml
    description: "Provisions VPCs, transit gateway, attachments, and configures bastion SSH access"
related_demos:
  - slug: cloud-peer-networking
    description: "Alternative direct-peering topology for simpler two-VPC setups"
  - slug: cloud-create-vpc
    description: "Standalone VPC creation for simpler setups"
---

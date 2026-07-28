---
layout: demo-detail
demo_slug: windows-ad-join-domain
description: >-
  Joins Windows hosts to an existing Active Directory domain. Sets the DNS
  client to point at the domain controller, creates an OU, updates the
  hostname, and performs the domain join.
prerequisites:
  - "An existing AD domain (created by <strong>WINDOWS | AD | Create Domain</strong>)"
  - "Domain controller private IP accessible from target hosts"
job_templates:
  - name: "WINDOWS | AD | Join Domain"
    playbook: windows/join_ad_domain.yml
    description: "Configures DNS, creates OU, updates hostname, and joins the host to the domain"
related_demos:
  - slug: windows-ad-create-domain
    description: "Create the domain before joining hosts"
  - slug: windows-ad-new-user
    description: "Create users in the domain after hosts are joined"
---

---
layout: demo-detail
demo_slug: windows-ad-create-domain
prerequisites:
  - "A Windows Server VM not yet joined to a domain"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
job_templates:
  - name: "WINDOWS | AD | Create Domain"
    playbook: windows/create_ad_domain.yml
    description: "Sets admin password, updates hostname, creates AD forest, and reboots"
related_demos:
  - slug: windows-ad-join-domain
    description: "Join additional hosts to the domain after creation"
  - slug: windows-setup-ad-domain
    description: "Full workflow that automates the entire AD setup"
---

Promotes a Windows Server to a domain controller and creates a new Active Directory forest. Sets the local admin password, updates the hostname, creates the domain, and reboots. The default domain is ansible.local.

_Promote a server to domain controller and create an AD forest_

---
layout: demo-detail
demo_slug: windows-ad-new-user
description: >-
  Creates a new Active Directory user with full attributes -- name,
  department, company, address, phone, and group memberships. Generates a
  random temporary password. Demonstrates a helpdesk self-service portal for
  user provisioning.
prerequisites:
  - "An Active Directory domain (deployed by <strong>Setup Active Directory Domain</strong> workflow)"
  - "Domain controller accessible via WinRM"
survey_prompts:
  - question: "First Name"
    variable: firstname
    type: text
    required: "Yes"
  - question: "Surname"
    variable: surname
    type: text
    required: "Yes"
  - question: "Street"
    variable: street
    type: text
    required: "Yes"
  - question: "City"
    variable: city
    type: text
    required: "Yes"
  - question: "Postal Code"
    variable: postal_code
    type: text
    required: "Yes"
  - question: "Telephone"
    variable: telephone_number
    type: text
    required: "Yes"
job_templates:
  - name: "WINDOWS | AD | New User"
    playbook: windows/helpdesk_new_user_portal.yml
    description: "Creates an AD user with full attributes, random password, and group memberships"
related_demos:
  - slug: windows-setup-ad-domain
    description: "Set up the AD domain before creating users"
  - slug: windows-run-powershell
    description: "Query AD for the newly created user"
---

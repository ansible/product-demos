---
layout: demo-detail
demo_slug: windows-install-iis
prerequisites:
  - "Windows hosts in the <strong>Ansible Product Demos Inventory</strong>"
  - "WinRM connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "IIS Message"
    variable: iis_message
    type: textarea
    required: "Yes"
job_templates:
  - name: "WINDOWS | Install IIS"
    playbook: windows/install_iis.yml
    description: "Installs the IIS Web-Server feature, starts it, and deploys a custom index page"
related_demos:
  - slug: windows-patching
    description: "Patch Windows hosts after deploying applications"
  - slug: windows-test-connectivity
    description: "Verify WinRM is working before running demos"
---

Installs Internet Information Services (IIS) on Windows Server, starts the W3SVC service, and deploys a custom index.html page. The page content is provided via survey. A quick, visual demo of Windows application deployment with Ansible.

_Install IIS and deploy a custom web page_

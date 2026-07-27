---
layout: demo-detail
demo_slug: linux-compliance-report
prerequisites:
  - "RHEL hosts with at least 2 GB RAM"
  - "SSH connectivity via <strong>APD Machine Credential</strong>"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Compliance Profile"
    variable: compliance_profile
    type: multiplechoice
    required: "Yes"
  - question: "Use httpd to host reports locally?"
    variable: use_httpd
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "LINUX | Multi-profile Compliance Report"
    playbook: linux/multi_profile_compliance_report.yml
    description: "Runs OpenSCAP scan and generates an HTML compliance report on target hosts"
related_demos:
  - slug: linux-multi-profile-compliance
    description: "Apply compliance enforcement after reviewing the report"
  - slug: linux-compliance-workflow
    description: "Automated scan then enforce workflow that uses this report"
---

Runs an OpenSCAP scan against a selected compliance profile and generates an HTML report. Installs the scanner and security guide packages, evaluates the system against the profile, and publishes results as a browsable HTML report.

_Generate an OpenSCAP compliance report for any profile_

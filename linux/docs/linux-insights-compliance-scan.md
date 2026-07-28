---
layout: demo-detail
demo_slug: linux-insights-compliance-scan
description: >-
  Triggers a Red Hat Insights compliance scan on RHEL hosts. Uses the
  redhat.insights.compliance role to run the scan and upload results to the
  Insights compliance dashboard on console.redhat.com.
prerequisites:
  - "RHEL hosts registered with Red Hat Insights"
  - "Compliance profile assigned in Insights"
survey_prompts:
  - question: "Server Name or Pattern"
    variable: _hosts
    type: text
    required: "Yes"
  - question: "Compliance profile configured?"
    variable: compliance_profile_configured
    type: multiplechoice
    required: "Yes"
job_templates:
  - name: "LINUX | Insights Compliance Scan"
    playbook: linux/insights_compliance_scan.yml
    description: "Runs the Insights compliance scan and uploads results to console.redhat.com"
related_demos:
  - slug: linux-register-insights
    description: "Register hosts with RHSM before running Insights scans"
  - slug: linux-compliance-report
    description: "Local OpenSCAP scanning as an alternative to Insights"
---

---
layout: demo-detail
demo_slug: openshift-eda-install
description: >-
  Deploys an Event-Driven Ansible (EDA) Controller on OpenShift, connected to
  the same AAP instance. Uses the demo.openshift.eda_controller role to
  install and configure the operator and custom resource.
prerequisites:
  - "<strong>OpenShift Credential</strong> configured with API token"
  - "Cluster admin access to the target OpenShift cluster"
job_templates:
  - name: "OpenShift | EDA | Install Controller"
    playbook: openshift/eda/install.yml
    description: "Deploys the EDA Controller operator and creates the EDA instance on OpenShift"
related_demos:
  - slug: openshift-cnv-install
    description: "Install OpenShift Virtualization alongside EDA"
---

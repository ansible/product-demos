---
layout: demo-detail
demo_slug: openshift-dev-spaces
description: >-
  Deploys Red Hat OpenShift Dev Spaces on an OpenShift cluster. Creates the
  namespace, installs the operator via OLM subscription, and creates the
  CheCluster custom resource.
prerequisites:
  - "<strong>OpenShift Credential</strong> configured with API token"
  - "Cluster admin access to the target OpenShift cluster"
job_templates:
  - name: "OpenShift | Dev Spaces | Install"
    playbook: openshift/devspaces.yml
    description: "Creates the namespace, installs the Dev Spaces operator, and provisions the CheCluster instance"
related_demos:
  - slug: openshift-gitlab
    description: "Install GitLab alongside Dev Spaces for a full developer platform"
---

---
layout: demo-detail
demo_slug: openshift-gitlab
prerequisites:
  - "<strong>OpenShift Credential</strong> configured with API token"
  - "Cluster admin access"
  - "Sufficient cluster resources for GitLab"
job_templates:
  - name: "OpenShift | GitLab | Install"
    playbook: openshift/gitlab.yml
    description: "Installs cert-manager, deploys the GitLab operator, and creates a GitLab instance on OpenShift"
related_demos:
  - slug: openshift-dev-spaces
    description: "Install Dev Spaces alongside GitLab for a complete developer platform"
---

Deploys GitLab on an OpenShift cluster using the GitLab Operator. Installs cert-manager as a prerequisite, then deploys the GitLab operator and creates a GitLab instance.

_Deploy GitLab on OpenShift via the GitLab Operator_

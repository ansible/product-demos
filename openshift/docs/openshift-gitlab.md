---
layout: demo-detail
demo_slug: openshift-gitlab
---
# GitLab


Deploys GitLab on an OpenShift cluster using the GitLab Operator. Installs cert-manager as a prerequisite, then deploys the GitLab operator and creates a GitLab instance.

## Prerequisites

- <strong>OpenShift Credential</strong> configured with API token
- Cluster admin access
- Sufficient cluster resources for GitLab

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ GitLab ǀ Install | [`openshift/gitlab.yml`](https://github.com/ansible/product-demos/blob/main/openshift/gitlab.yml) | Installs cert-manager, deploys the GitLab operator, and creates a GitLab instance on OpenShift |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [Dev Spaces](/product-demos/demos/openshift-dev-spaces/) | Install Dev Spaces alongside GitLab for a complete developer platform |

# Dev Spaces


Deploys Red Hat OpenShift Dev Spaces on an OpenShift cluster. Creates the namespace, installs the operator via OLM subscription, and creates the CheCluster custom resource.

## Prerequisites

- **OpenShift Credential** configured with API token
- Cluster admin access to the target OpenShift cluster

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| OpenShift ǀ Dev Spaces ǀ Install | [`openshift/devspaces.yml`](../devspaces.yml) | Creates the namespace, installs the Dev Spaces operator, and provisions the CheCluster instance |

## Related demos

| Demo | Description |
|------|-------------|
| ⎈ [GitLab](./openshift-gitlab.md) | Install GitLab alongside Dev Spaces for a full developer platform |

# demo.openshift

Local collection containing roles used by the [OpenShift demos](../../../../openshift/README.md) in ansible-product-demos.

This collection is not published to Ansible Galaxy or Automation Hub; it exists solely to organize roles used by playbooks in this repository under the `demo.openshift` namespace.

## Contents

### Roles

| Role | Description |
|------|-------------|
| [cluster_config](roles/cluster_config/README.md) | Configure OpenShift Operators (catalog sources, operator groups, and subscriptions), including support for VM migrations. |
| [eda_controller](roles/eda_controller/README.md) | Install Event-Driven Ansible (EDA) Controller on OpenShift. |
| [snapshot](roles/snapshot/README.md) | Create and restore OpenShift Virtualization (KubeVirt) VM snapshots. |
| [vault](roles/vault/README.md) | Deploy and configure HashiCorp Vault on OpenShift via Helm, with optional JWT, KV, and userpass auth. |

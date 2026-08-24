# demo.infrastructure

Local collection containing roles used by the [Infrastructure demos](../../../../infrastructure/README.md) in ansible-product-demos.

This collection is not published to Ansible Galaxy or Automation Hub; it exists solely to organize roles used by playbooks in this repository under the `demo.infrastructure` namespace.

## Contents

### Roles

| Role | Description |
|------|-------------|
| [vault](roles/vault/README.md) | Deploy and configure HashiCorp Vault on OpenShift via Helm, with optional JWT, KV, and userpass auth. |

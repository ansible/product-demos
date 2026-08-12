# demo.satellite

Local collection containing roles used by the [Satellite demos](../../../../satellite/README.md) in ansible-product-demos.

This collection is not published to Ansible Galaxy or Automation Hub; it exists solely to organize roles used by playbooks in this repository under the `demo.satellite` namespace.

## Contents

### Roles

| Role | Description |
|------|-------------|
| [register_host](roles/register_host/README.md) | Register a RHEL host with Red Hat Satellite via an activation key, enable repos, and install remote execution tooling. |
| [scap_client](roles/scap_client/README.md) | Configure a client to run OpenSCAP compliance policies using configuration obtained from Satellite/Foreman. |

# demo.openshift.vault

Deploy, initialize, and configure HashiCorp Vault on OpenShift via the HashiCorp Helm chart. Supports AAP OIDC JWT workload identity, KV secrets, and userpass auth.

Adapted from [demo.zero_trust.vault](https://github.com/zjleblanc/ansible-zero-trust/tree/main/collections/ansible_collections/demo/zero_trust/roles/vault), simplified to target OpenShift only (the RPM and Podman Quadlet install paths from the upstream role are not included here).

Invoke with `include_role` and `tasks_from` -- do not call the role without selecting an entry point.

```yaml
- name: Deploy Vault on OpenShift
  ansible.builtin.include_role:
    name: demo.openshift.vault
    tasks_from: install_k8s
```

Typical sequence: `install_k8s` -> `configure_jwt_auth` (optional) -> `configure_kv_engine` (optional) -> `configure_userpass_auth` (optional). `install_k8s` always deploys Helm chart "dev" mode, so Vault is already initialized and unsealed -- there is no separate init step.

Because the demo targets OpenShift from `localhost` (no managed host filesystem), connection details and generated userpass credentials are exported with `ansible.builtin.set_stats` for AAP job artifact visualization. **Demo only -- do not publish tokens or passwords via `set_stats` in production;** store them in a credential or secret manager instead.

Repo playbook: [`openshift/vault.yml`](../../../../../../openshift/vault.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: OpenShift cluster access
- `kubernetes.core` collection
- `oc` and Helm CLI available to the controller
- An attached "OpenShift Credential" (type `OpenShift or Kubernetes API Bearer Token`) so `K8S_AUTH_HOST` / `K8S_AUTH_API_KEY` / `K8S_AUTH_VERIFY_SSL` are injected. `kubernetes.core` / Helm modules use those env vars directly; `oc exec` (vault CLI wrapper) gets the same values as `--server` / `--token` / `--insecure-skip-tls-verify` (no kubeconfig)
- For `configure_jwt_auth`: an attached "AAP Credential" (type `Red Hat Ansible Automation Platform`) so `vault_jwt_oidc_discovery_url` can be derived from the injected `CONTROLLER_HOST` environment variable

## Role Variables

Defaults live in `defaults/main.yml`. See that file for the full list of variables and their descriptions; the OpenShift-relevant highlights are:

| Variable | Default | Description |
| --- | --- | --- |
| `vault_k8s_namespace` | `vault` | Kubernetes namespace for the Vault release |
| `vault_k8s_release_name` | `vault` | Helm release name |
| `vault_k8s_dev_root_token` | `root` | Root token for the Helm chart "dev" mode Vault |
| `vault_k8s_route_enabled` | `true` | Create an OpenShift Route for external access |
| `vault_k8s_cluster_base_url` | derived | Cluster or apps domain; discovered from the OpenShift ingress when unset; leading `apps.` stripped before Route host composition |
| `vault_validate_certs` | `false` | TLS verify for the Route health check (`uri`); off by default for demo self-signed router certs |
| `vault_jwt_oidc_discovery_url` | derived | `{{ CONTROLLER_HOST }}/o`, from the AAP Credential's injected `CONTROLLER_HOST` |

This role always installs Vault in the Helm chart's [`dev` server mode](https://developer.hashicorp.com/vault/docs/concepts/dev-server): a single replica with in-memory storage that comes up already initialized and unsealed with a fixed root token (`vault_k8s_dev_root_token`), so there's no separate init/unseal step. Data does not persist across pod restarts -- **this mode is only meant for demos and development, not production use.**

Two further simplifying assumptions:

- The only cluster-specific input the role needs is `vault_k8s_cluster_base_url` (e.g. `cluster.example.com` or `apps.cluster.example.com`), and it is normally discovered automatically from the OpenShift ingress domain. A leading `apps.` is stripped, then the Route host is composed as `{{ vault_k8s_release_name }}.apps.{{ vault_k8s_cluster_base_url }}` for `vault_fqdn` / `vault_addr`.
- The CLI is always `oc` -- there is no `kubectl` support or toggle.

## Entry points

| Entry point | Description |
| --- | --- |
| `install_k8s` | Deploy Vault via the HashiCorp Helm chart in dev mode (namespace, Helm repo/release, optional OpenShift Route, pod wait, HTTP health). Sets `vault_cli` (`oc exec` wrapper), `vault_cli_addr`, `vault_addr`, `vault_fqdn`, and `vault_token`. Exports `vault_addr` / `vault_fqdn` / `vault_root_token` via `set_stats` (demo only).<br><br>Kubernetes/Helm automation originally by [Matt Fernandez](https://github.com/l3acon/aap-vault). |
| `configure_jwt_auth` | Enable JWT auth for AAP OIDC workload identity with static and dynamic (templated) roles/policies. Requires `vault_jwt_oidc_discovery_url`. |
| `configure_kv_engine` | Enable the KV v2 secrets engine and seed sample secrets for e2e testing. |
| `configure_userpass_auth` | Enable userpass auth and create users from `files/vault_users.json`. Exports generated passwords via `set_stats` (demo only). |
| `uninstall` | Remove the Vault Helm release, OpenShift Route, and namespace. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- **Zachary LeBlanc** -- author of the original upstream role, [demo.zero_trust.vault](https://github.com/zjleblanc/ansible-zero-trust/tree/main/collections/ansible_collections/demo/zero_trust/roles/vault); this role is adapted from it for `demo.openshift`.
- **Matt Fernandez** -- original author of the Kubernetes/Helm deployment automation used in `tasks/install_k8s.yml`, from [l3acon/aap-vault](https://github.com/l3acon/aap-vault) (`deploy-vault.yml`).

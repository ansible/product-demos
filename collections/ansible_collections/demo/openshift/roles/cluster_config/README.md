# demo.openshift.cluster_config

Configure OpenShift Operators via OLM -- namespaces, OperatorGroups, Subscriptions, optional CatalogSources, and operator-specific extra resources (for example HyperConverged for CNV).

By default the role installs OpenShift Virtualization (CNV). Additional operators can be declared in `cluster_config_operators` with matching `cluster_config_<name>` dictionaries.

```yaml
- name: Install the CNV operator
  ansible.builtin.include_role:
    name: demo.openshift.cluster_config
```

Optional entry points select narrower task files with `tasks_from` (see [Entry points](#entry-points)).

Repo playbook: [`openshift/cnv/install.yml`](../../../../../../openshift/cnv/install.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: OpenShift cluster access
- `redhat.openshift` and `kubernetes.core` collections
- An attached "OpenShift Credential" (type `OpenShift or Kubernetes API Bearer Token`) so `K8S_AUTH_HOST` / `K8S_AUTH_API_KEY` / `K8S_AUTH_VERIFY_SSL` are injected
- Cluster-admin (or equivalent) rights to create namespaces, OperatorGroups, Subscriptions, and CatalogSources

## Role Variables

Defaults live in `defaults/main.yml`. See that file for the full list of variables and their descriptions; the highlights are:

| Variable | Default | Description |
| --- | --- | --- |
| `cluster_config_operators` | `[cnv]` | List of operator short names to configure; each name must have a matching `cluster_config_<name>` dict |
| `cluster_config_cnv` | see defaults | CNV operator config: namespace, OperatorGroup, Subscription, and HyperConverged `extra_resources` |
| `cluster_config_catalog_sources` | unset | Optional list of custom CatalogSource definitions (used by the `operators/catalog_sources` entry point) |
| `cluster_config_<operator>` | — | Per-operator dict with `namespace`, `operator_group`, `subscription`, optional `checkplan`, and optional `extra_resources` |

For each name in `cluster_config_operators`, the role looks up `vars['cluster_config_' + name]`, applies the namespace / OperatorGroup / Subscription templates, optionally waits for the InstallPlan (`checkplan: true`), then applies any `extra_resources`.

Example of adding OADP alongside CNV:

```yaml
cluster_config_operators:
  - cnv
  - oadp

cluster_config_oadp_namespace: openshift-adp
cluster_config_oadp:
  namespace:
    name: "{{ cluster_config_oadp_namespace }}"
  operator_group:
    name: redhat-oadp-operator-group
    target_namespaces:
      - "{{ cluster_config_oadp_namespace }}"
  subscription:
    name: redhat-oadp-operator-subscription
    spec_name: redhat-oadp-operator
```

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Configure every operator listed in `cluster_config_operators` (`operators/operator_config.yml`). |
| `operators/catalog_sources` | Apply custom CatalogSource manifests from `cluster_config_catalog_sources` (for example mirrored registries). Skips when the variable is undefined. |
| `operators/node-health-check` | Install the Node Health Check operator into `openshift-workload-availability`. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.openshift`](../../README.md) for the OpenShift automation demos in this repository.

# demo.openshift.eda_controller

Install Event-Driven Ansible (EDA) Controller on OpenShift via the AAP EDA operator custom resource, wait for the Route to become healthy, and create a ClusterRoleBinding for rulebook activations.

Mostly adapted from [redhat-cop/agnosticd](https://github.com/redhat-cop/agnosticd/).

```yaml
- name: Deploy EDA Controller on OpenShift
  ansible.builtin.include_role:
    name: demo.openshift.eda_controller
```

The role creates the admin password Secret and `EDA` CR, discovers the OpenShift Route host, waits until the EDA API answers, then binds the default service account for activations. Admin login is `admin` with the same password as the AAP Controller admin (`CONTROLLER_PASSWORD`).

Repo playbook: [`openshift/eda/install.yml`](../../../../../../openshift/eda/install.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: OpenShift cluster access with the AAP EDA operator available (typically already installed in the AAP namespace)
- `kubernetes.core` collection
- An attached "OpenShift Credential" (type `OpenShift or Kubernetes API Bearer Token`) so `K8S_AUTH_HOST` / `K8S_AUTH_API_KEY` / `K8S_AUTH_VERIFY_SSL` are injected
- An attached "AAP Credential" (type `Red Hat Ansible Automation Platform`) so `CONTROLLER_HOST` and `CONTROLLER_PASSWORD` are injected -- used for `automation_server_url` on the EDA CR and for the admin password / readiness check

## Role Variables

Defaults live in `defaults/main.yml`. See that file for the full list of variables and their descriptions; the highlights are:

| Variable | Default | Description |
| --- | --- | --- |
| `eda_controller_project` | `aap` | Namespace where the EDA instance is created |
| `eda_controller_project_app_name` | `eda-controller` | Name of the EDA custom resource and related Route / Secret |
| `eda_controller_admin_password` | unset | Optional override; when unset the admin Secret uses `CONTROLLER_PASSWORD` from the AAP Credential |
| `eda_controller_cluster_rolebinding_name` | `eda_default` | Name of the ClusterRoleBinding for rulebook activations |
| `eda_controller_cluster_rolebinding_role` | `cluster-admin` | ClusterRole bound to the EDA activation service account |

The EDA CR sets `automation_server_url` from the injected `CONTROLLER_HOST` environment variable so the EDA instance points at the same AAP Controller that launched the job.

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Create admin Secret and EDA CR, wait for Route and API readiness, create ClusterRoleBinding, and print the EDA URL / login hints. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- **Mitesh Sharma** (`mitsharm@redhat.com`) -- role author (see `meta/main.yml`).
- Adapted from workload content in [redhat-cop/agnosticd](https://github.com/redhat-cop/agnosticd/).

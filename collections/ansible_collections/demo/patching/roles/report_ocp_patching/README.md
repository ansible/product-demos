# demo.patching.report_ocp_patching

Deploy a self-contained OpenShift-hosted patching report: an httpd Deployment backed by a ConfigMap (landing page, inventory report, patch report, CSS, and logo assets), a Service, and an edge-terminated Route -- for OpenShift Virtualization (CNV) patching demos where there is no dedicated Linux report server VM.

```yaml
- name: Publish landing page
  ansible.builtin.include_role:
    name: demo.patching.report_ocp_patching
```

Unlike the other reporting roles (which copy files onto an existing Apache/IIS server built by `demo.patching.report_server`), this role renders all report content into a single `ConfigMap` and runs it behind a Route -- no separate report server host is required.

Repo playbook: [`openshift/cnv/patch.yml`](../../../../../../openshift/cnv/patch.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: `localhost`, with OpenShift cluster access (run after `demo.patching.patch_linux` against the CNV-hosted VMs)
- `redhat.openshift` collection (`k8s`)
- An attached "OpenShift Credential" (type `OpenShift or Kubernetes API Bearer Token`) so `K8S_AUTH_HOST` / `K8S_AUTH_API_KEY` / `K8S_AUTH_VERIFY_SSL` are injected
- Access to the `registry.redhat.io/rhel8/httpd-24` image from the cluster

## Role Variables

This role has no `defaults/main.yml` or non-empty `vars/main.yml`; the namespace (`patching-report`) and resource names are currently hardcoded in `tasks/main.yml` and `templates/resources.yaml.j2`.

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Create the `patching-report` namespace, apply the rendered `ConfigMap`/`Deployment`/`Service`/`Route` from `templates/resources.yaml.j2`, and print the report Route URL. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the OpenShift CNV patching demos in this repository.

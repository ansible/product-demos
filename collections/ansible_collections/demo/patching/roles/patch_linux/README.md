# demo.patching.patch_linux

Upgrade all packages on a RHEL host via `yum`/`dnf` (excluding a configurable package list) and reboot automatically if the kernel or a core library requires it.

```yaml
- name: Include patching role
  ansible.builtin.include_role:
    name: demo.patching.patch_linux
```

Package/service facts are gathered first (for later reporting by `demo.patching.report_linux` / `demo.patching.report_linux_patching`), then `needs-restarting -r` decides whether a reboot is required; the reboot only runs when `allow_reboot` is `true`.

Repo playbooks: [`linux/patching.yml`](../../../../../../linux/patching.yml), [`openshift/cnv/patch.yml`](../../../../../../openshift/cnv/patch.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: RHEL host with `become` and either `yum` or `dnf`
- `yum-utils` installed on the target (provides `needs-restarting`; the calling playbooks install it before running this role)

## Role Variables

Defaults live in `defaults/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `exclude_packages` | `authselect`, `authselect-compat`, `authselect-libs`, `fprintd-pam` | Packages excluded from the `yum`/`dnf` upgrade (`state: latest`) |
| `allow_reboot` | `true` | When `true` and `needs-restarting -r` reports a pending reboot, the host is rebooted |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Gather package/service facts, upgrade all packages (`yum` or `dnf`, excluding `exclude_packages`), check for a required reboot, and reboot if `allow_reboot` is `true`. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the Linux patching demos in this repository.

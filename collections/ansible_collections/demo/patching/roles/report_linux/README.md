# demo.patching.report_linux

Build an HTML inventory report of a Linux host's installed packages and running services (from facts gathered by `demo.patching.patch_linux`), and copy it -- with shared CSS/logo assets -- to the report server's web root.

```yaml
- name: Build report server
  ansible.builtin.include_role:
    name: "{{ item }}"
  loop:
    - demo.patching.report_server
    - demo.patching.report_linux
    - demo.patching.report_linux_patching
```

Run after `demo.patching.report_server` (so the destination directory and web server exist) and after `demo.patching.patch_linux` on the target host (so package/service facts are populated).

Repo playbook: [`linux/patching.yml`](../../../../../../linux/patching.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: Linux host with an Apache document root already created (see `demo.patching.report_server`)
- Package/service facts populated (`ansible.builtin.package_facts` / `service_facts`, run by `demo.patching.patch_linux`)

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `/var/www/html/reports` | Destination directory for `linux.html`, CSS, and logo assets |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Template `linux.html` from package/service facts, copy CSS and logo assets, and print the report URL. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the Linux patching report demos in this repository.

# demo.patching.build_report_windows

Build an HTML inventory report of a Windows host's installed packages and running services, and copy it -- with shared CSS/logo assets -- to the report server's web root.

```yaml
- name: Build Windows inventory report
  ansible.builtin.include_role:
    name: demo.patching.build_report_windows
```

Not currently referenced by a repo playbook; `demo.patching.report_windows` is the actively used equivalent (and correctly uses `ansible.windows.win_template` / `win_copy` rather than the Linux `ansible.builtin` modules used here). Kept for backward compatibility -- prefer `demo.patching.report_windows` for new work.

## Requirements

- ansible-core >= 2.16.0
- Target: as templated, a Windows web root (`C:\Inetpub\wwwroot`), but the tasks use `ansible.builtin.template` / `ansible.builtin.copy`, which only work against a POSIX-style connection to that path
- Package/service facts populated (`ansible.builtin.package_facts` / `service_facts`)

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `/var/www/html` | Destination directory for `windows.html`, CSS, and logo assets |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Template `windows.html` from package/service facts, copy CSS and logo assets, and print the report URL. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the Windows patching report demos in this repository.

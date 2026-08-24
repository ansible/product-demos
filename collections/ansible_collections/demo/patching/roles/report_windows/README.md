# demo.patching.report_windows

Build an HTML inventory report of a Windows host's installed packages and running services (from facts gathered by `demo.patching.patch_windows`), and copy it -- with shared CSS/logo assets -- to the report server's web root.

```yaml
- name: Install report server
  ansible.builtin.include_role:
    name: "{{ item }}"
  loop:
    - demo.patching.report_server
    - demo.patching.report_windows
    - demo.patching.report_windows_patching
```

Run after `demo.patching.report_server` (so IIS and the destination directory exist) and after `demo.patching.patch_windows` on the target host (so package/service facts are populated).

Repo playbook: [`windows/patching.yml`](../../../../../../windows/patching.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: Windows host with the IIS document root already created (see `demo.patching.report_server`)
- `ansible.windows` collection (`win_template`, `win_copy`)
- Package/service facts populated by `demo.patching.patch_windows` (`demo.patching.win_scan_packages` / `win_scan_services`)

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `C:\Inetpub\wwwroot\reports` | Destination directory for `windows.html`, CSS, and logo assets |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Template `windows.html` from package/service facts and copy CSS and logo assets. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the Windows patching report demos in this repository.

# demo.patching.build_report_windows_patch

Build an HTML patching report for a Windows host, and copy it -- with shared CSS/logo assets -- to the report server's web root.

```yaml
- name: Build Windows patch report
  ansible.builtin.include_role:
    name: demo.patching.build_report_windows_patch
```

Not currently referenced by a repo playbook; `demo.patching.report_windows_patching` is the actively used equivalent (and correctly uses `ansible.windows.win_template` / `win_copy` rather than the Linux `ansible.builtin` modules used here). Kept for backward compatibility -- prefer `demo.patching.report_windows_patching` for new work.

## Requirements

- ansible-core >= 2.16.0
- Target: as templated, a Windows web root (`C:\Inetpub\wwwroot`), but the tasks use `ansible.builtin.template` / `ansible.builtin.copy`, which only work against a POSIX-style connection to that path
- A `patchresult` fact on the target host (`templates/report.j2` reads `hostvars[windows_host].patchresult`); note neither `demo.patching.patch_windows` (`patch_windows_patchingresult`) nor `demo.patching.report_windows_patching`'s template (`patchingresult`) use this exact name

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `/var/www/html` | Destination directory for `windowspatch.html`, CSS, and logo asset |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Template `windowspatch.html`, copy CSS and the logo asset, and print the report URL. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the Windows patching report demos in this repository.

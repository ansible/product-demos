# demo.patching.report_linux_patching

Build an HTML patching report for a Linux host (`yum`/`dnf` upgrade results from `demo.patching.patch_linux`), and copy it -- with shared CSS/logo assets -- to the report server's web root.

```yaml
- name: Build report server
  ansible.builtin.include_role:
    name: "{{ item }}"
  loop:
    - demo.patching.report_server
    - demo.patching.report_linux
    - demo.patching.report_linux_patching
```

Run after `demo.patching.report_server` and after `demo.patching.patch_linux` on the target host so the `patch_linux_patchingresult_yum` / `patch_linux_patchingresult_dnf` facts used by the report template are populated. An optional (currently commented out) `community.general.mail` task can email the rendered report.

Repo playbook: [`linux/patching.yml`](../../../../../../linux/patching.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: Linux host with an Apache document root already created (see `demo.patching.report_server`)
- Patching result facts registered by `demo.patching.patch_linux`

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `/var/www/html/reports` | Destination directory for `linuxpatch.html`, CSS, and logo assets |
| `email_from` | `tower@shadowman.dev` | `From` address for the optional (disabled) e-mail task |
| `to_emails` | `alex@shadowman.dev,tower@shadowman.dev` | Comma-separated recipient list for the optional (disabled) e-mail task |
| `to_emails_list` | `{{ to_emails.split(',') }}` | `to_emails` split into a list |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Template `linuxpatch.html` from patching-result facts, copy CSS and logo assets, and print the report URL. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the Linux patching report demos in this repository.

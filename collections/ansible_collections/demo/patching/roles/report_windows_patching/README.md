# demo.patching.report_windows_patching

Build an HTML patching report for a Windows host (Windows Update results from `demo.patching.patch_windows`), and copy it -- with shared CSS/logo assets -- to the report server's web root.

```yaml
- name: Install report server
  ansible.builtin.include_role:
    name: "{{ item }}"
  loop:
    - demo.patching.report_server
    - demo.patching.report_windows
    - demo.patching.report_windows_patching
```

Run after `demo.patching.report_server` and after `demo.patching.patch_windows` on the target host. **Note:** `templates/report.j2` reads `hostvars[windows_host].patchingresult`, but `demo.patching.patch_windows` registers the result as `patch_windows_patchingresult` -- as shipped, the template's `is defined` guard means the updates table silently renders empty rather than erroring.

Repo playbook: [`windows/patching.yml`](../../../../../../windows/patching.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: Windows host with the IIS document root already created (see `demo.patching.report_server`)
- `ansible.windows` collection (`win_template`, `win_copy`)
- Patching result facts registered by `demo.patching.patch_windows`

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `C:\Inetpub\wwwroot\reports` | Destination directory for `windowspatch.html`, CSS, and logo assets |
| `email_from` | `tower@shadowman.dev` | Reserved for future e-mail notification support (unused by current tasks) |
| `to_emails` | `alex@shadowman.dev,tower@shadowman.dev` | Reserved for future e-mail notification support (unused by current tasks) |
| `to_emails_list` | `{{ to_emails.split(',') }}` | `to_emails` split into a list |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Template `windowspatch.html` from Windows Update result facts and copy CSS and logo assets. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the Windows patching report demos in this repository.

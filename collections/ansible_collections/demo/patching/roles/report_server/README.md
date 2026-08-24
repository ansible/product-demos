# demo.patching.report_server

Configure the shared report web server -- Apache on Linux, IIS on Windows -- that hosts the HTML reports built by the other `demo.patching` reporting roles, and publish the landing page that links to them.

```yaml
- name: Build report server
  ansible.builtin.include_role:
    name: "{{ item }}"
  loop:
    - demo.patching.report_server
    - demo.patching.report_linux
    - demo.patching.report_linux_patching

- name: Publish landing page
  ansible.builtin.include_role:
    name: demo.patching.report_server
    tasks_from: linux_landing_page
```

Run `main` first to install/start the web server and create the reports directory, then run the individual `build_report_*` / `report_*` roles to populate `*.html` files, then run the `linux_landing_page` or `windows_landing_page` entry point to (re)generate `index.html` linking to whatever reports currently exist.

Repo playbooks: [`linux/patching.yml`](../../../../../../linux/patching.yml), [`windows/patching.yml`](../../../../../../windows/patching.yml), [`network/report.yml`](../../../../../../network/report.yml), [`network/backup.yml`](../../../../../../network/backup.yml).

## Requirements

- ansible-core >= 2.16.0
- Target (Linux): RHEL host with `become` and `dnf` (installs `httpd`)
- Target (Windows): Windows host with the IIS `Web-Server` feature available
- `ansible.windows` collection for the Windows entry points

## Role Variables

Defaults live in `vars/Linux.yml` (Linux) / `vars/Win32NT.yml` (Windows), selected automatically via `include_vars: "{{ ansible_system }}.yml"`.

| Variable | Default (Linux) | Default (Windows) | Description |
| --- | --- | --- | --- |
| `doc_root` | `/var/www/html` | `C:\Inetpub\wwwroot` | Web server document root |
| `reports_dir` | `reports` | `reports` | Subdirectory under `doc_root` where report HTML files live |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Include Linux tasks (`apache.yml`) or Windows tasks (`iis.yml`) based on `ansible_system`. |
| `apache.yml` | Install and start `httpd`, create the reports directory, and enable directory indexing via `.htaccess`. |
| `iis.yml` | Install and start the `Web-Server` (IIS) feature, create the reports directory, and enable directory browsing. |
| `linux_landing_page` | Find existing `*.html` reports and template `index.html` linking to them (Apache). |
| `windows_landing_page` | Find existing `*.html` reports and template `index.html` linking to them (IIS). |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the patching report-server demos in this repository.

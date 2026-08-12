# demo.cloud.build_report_linux

Install Apache on a Linux host, template a cloud infrastructure HTML report, and print the public URL to view it -- used as the report server for the AWS cloud demos when the report is hosted on a VM rather than S3.

```yaml
- name: Load report to host on Linux
  ansible.builtin.include_role:
    name: demo.cloud.build_report_linux
  when: inventory_hostname != 'localhost'
```

Run after `demo.cloud.retrieve_info` and `demo.cloud.template` have gathered facts and rendered `index.html`; this role installs and configures the actual Apache server and publishes the assets. Public IP is looked up from `https://checkip.amazonaws.com` to build the printed URL.

Repo playbook: [`cloud/cloud_report.yml`](../../../../../../cloud/cloud_report.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: RHEL host with `become` and `dnf`
- `ansible.posix` collection (`seboolean`)
- Outbound network access from the target to `https://checkip.amazonaws.com` (used only to print the report URL; failures are ignored)

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `/var/www/html/` | Apache document root where the report, CSS, and images are copied |
| `web_host` | `ansible-1` | Informational hostname referenced when printing host vars |
| `web_port` | `8088` | Port Apache is reconfigured to listen on |
| `vendor` | `{ios: Cisco, nxos: Cisco, iosxr: Cisco, junos: Juniper, eos: Arista}` | Unused by this role's own tasks; shared boilerplate vars file copied from the network reporting roles |
| `transport` | `{cliconf: network_cli, netconf: netconf, httpapi: httpapi}` | Unused by this role's own tasks; shared boilerplate vars file copied from the network reporting roles |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Install and start Apache on `web_port`, template `index.html`, copy CSS/image assets, and print the report URL. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.cloud`](../../README.md) for the AWS cloud reporting demos in this repository.

# demo.cloud.template

Render the multi-region cloud infrastructure HTML report (`index.html`) from the per-region facts gathered by `demo.cloud.retrieve_info`, and copy its CSS/image assets alongside it.

```yaml
- name: Template report into HTML
  ansible.builtin.include_role:
    name: demo.cloud.template
```

Run after `demo.cloud.retrieve_info` (so `all_ec2_regions` and the per-region facts exist) and before `demo.cloud.build_report_linux` / `demo.cloud.build_report_s3` (so there is an `index.html` to publish).

Repo playbook: [`cloud/cloud_report.yml`](../../../../../../cloud/cloud_report.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: `localhost` (all tasks are `delegate_to: localhost`, `run_once: true`)
- Per-region facts populated by `demo.cloud.retrieve_info`

## Role Variables

Defaults live in `vars/main.yml`. These are largely shared boilerplate with the network/Linux report roles and are not all used by this role's own template.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `/var/www/html/` | Unused by this role's own tasks (destination is always `{{ playbook_dir }}/index.html`); kept from the shared vars file |
| `web_host` | `ansible-1` | Unused by this role's own tasks |
| `web_port` | `8088` | Unused by this role's own tasks |
| `vendor` | `{ios: Cisco, nxos: Cisco, iosxr: Cisco, junos: Juniper, eos: Arista}` | Unused by this role's own tasks |
| `transport` | `{cliconf: network_cli, netconf: netconf, httpapi: httpapi}` | Unused by this role's own tasks |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Template `report.j2` to `{{ playbook_dir }}/index.html` and copy the role's `files/` (CSS, logos) alongside it. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.cloud`](../../README.md) for the AWS cloud reporting demos in this repository.

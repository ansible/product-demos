# demo.patching.build_report_network

Build an HTML report of network device configuration (interfaces, LACP, VLANs, OSPF, BGP, static routes) from resource facts gathered by `cisco.ios`/`cisco.nxos`/`cisco.iosxr`, and copy it -- with shared CSS/logo assets -- to the report server's web root.

Re-written from [network-automation/toolkit](https://github.com/network-automation/toolkit/blob/master/roles/build_report/tasks/main.yml).

```yaml
- name: Build report server
  ansible.builtin.include_role:
    name: "{{ item }}"
  loop:
    - demo.patching.report_server
    - demo.patching.build_report_network
```

Run after `cisco.ios.ios_facts` / `cisco.nxos.nxos_facts` / `cisco.iosxr.iosxr_facts` have gathered `gather_network_resources: all`, and after `demo.patching.report_server` has created the report directory/web server.

Repo playbook: [`network/report.yml`](../../../../../../network/report.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: the report server (Linux/Apache), with `hostvars` available for the network devices reported on
- Network resource facts already gathered for the devices being reported on (`cisco.ios`, `cisco.nxos`, and/or `cisco.iosxr` collections)

## Role Variables

Defaults live in `vars/main.yml`.

| Variable | Default | Description |
| --- | --- | --- |
| `file_path` | `{{ web_path \| default('/var/www/html/reports') }}` | Destination directory for `network.html`, CSS, and logo assets |
| `vendor` | `{ios: Cisco, nxos: Cisco, iosxr: Cisco, junos: Juniper, eos: Arista}` | Maps `ansible_network_os` to a display vendor name in the report |
| `transport` | `{cliconf: Network_CLI, netconf: NETCONF, nxapi: NX-API}` | Maps connection plugin to a display transport name in the report |

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Create the report directory, template `network.html` from gathered network resource facts, copy CSS and logo assets, and print the report URL. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.patching`](../../README.md) for the network reporting demos in this repository.
- Adapted from [network-automation/toolkit](https://github.com/network-automation/toolkit).

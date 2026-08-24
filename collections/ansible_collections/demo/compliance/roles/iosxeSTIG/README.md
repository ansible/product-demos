# demo.compliance.iosxeSTIG

Remediate a Cisco IOS XE device against the DISA STIG for Cisco IOS XE Router NDM/RTR (`U_Cisco_IOS-XE_Router_NDM_STIG_V2R1` and `..._RTR_STIG_V2R1`, 33 rules), driven entirely by `ios_config`/`ios_command`.

```yaml
- name: IOS XE Compliance
  hosts: "{{ _hosts | default('ios') }}"
  vars:
    ignore_all_errors: false
    ansible_command_timeout: 60
  roles:
    - demo.compliance.iosxeSTIG
```

Every rule is gated by its own `iosxeSTIG_stigrule_<ID>_Manage` boolean (default `true`, except a few site-specific rules noted below) plus companion `_Lines`/`_Text` variables holding the config to enforce. Rules are tagged `stigrule_<ID>` for selective runs (`--tags`). All tasks run with `ignore_errors: "{{ ignore_all_errors }}"`, a variable the role does **not** default -- the caller must set it. A `save configuration` handler (`write memory`) fires when any task changes state, but only runs if `iosxeSTIG_save_configuration_Manage` is `true` (default `false`).

The role ships a whitelist-required `stig_xml` callback plugin (`callback_plugins/stig_xml.py`) that watches for tasks named `stigrule_<ID>...`, maps `changed` to XCCDF fail / `ok` to pass, and writes an XCCDF `TestResult` XML against the shipped benchmark (`files/*.xml`, or `STIG_PATH`) to `XML_PATH` (or a temp file) when enabled (for example `ANSIBLE_CALLBACKS_ENABLED=stig_xml`).

Repo playbook: [`network/compliance.yml`](../../../../../../network/compliance.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: Cisco IOS XE device reachable via `network_cli`
- `cisco.ios` collection
- Caller must set `ignore_all_errors` (used by every task); the repo playbook sets it to `false`

## Role Variables

Defaults live in `defaults/main.yml` (~102 variables). Each of the 33 STIG rules has an `iosxeSTIG_stigrule_<ID>_Manage` toggle plus rule-specific value variables (`_Lines`, `_Text`, etc.); see that file for the complete list. Site-specific rules default to **disabled** since they require environment-specific values:

| Variable | Default | Description |
| --- | --- | --- |
| `iosxeSTIG_stigrule_215826_Manage` | `false` | Password policy enforcement (site-specific) |
| `iosxeSTIG_stigrule_215837_Manage` | `false` | Central logging host configuration (site-specific) |
| `iosxeSTIG_stigrule_215838_Manage` | `false` | NTP server configuration (site-specific) |
| `iosxeSTIG_save_configuration_Manage` | `false` | Whether the `save configuration` handler runs `write memory` after changes |

Example of a typical rule pair:

```yaml
iosxeSTIG_stigrule_215814_Manage: true
iosxeSTIG_stigrule_215814_login_Text: |
  banner login ^C
  ... DoD warning banner text ...
  ^C
```

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Apply each enabled STIG rule via `ios_config`/`ios_command`, tagged `stigrule_<ID>`; notify `save configuration` on change. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.compliance`](../../README.md) for the network compliance demos in this repository.

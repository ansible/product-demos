# demo.compliance.win2022STIG

Remediate a Windows Server 2022 host against the DISA STIG for Microsoft Windows Server 2022 (`U_MS_Windows_Server_2022_STIG_V1R1`, 198 rules) -- registry settings, audit policy, user rights assignments, security policy, ACLs, and Windows feature state.

```yaml
- name: STIG a Windows 2022 Server
  hosts: "{{ HOSTS | default('os_windows') }}"
  vars:
    win2022STIG_stigrule_254269_Manage: false  # noqa var-naming
    win2022STIG_stigrule_254276_Manage: false  # noqa var-naming
  tasks:
    - name: Include win2022STIG role
      ansible.builtin.include_role:
        name: demo.compliance.win2022STIG
```

Every rule is gated by its own `win2022STIG_stigrule_<ID>_Manage` boolean (177 default `true`, 21 default `false` for site-specific rules -- for example NTP and account lockout/password policy) plus companion value variables. Rules are tagged `stigrule_<ID>` for selective runs (`--tags`). This role's `handlers/main.yml` is empty -- registry/policy modules apply changes directly, with no separate restart/reload step.

The role ships a whitelist-required `stig_xml` callback plugin (`callback_plugins/stig_xml.py`) that watches for tasks named `stigrule_<ID>...`, maps `changed` to XCCDF fail / `ok` to pass, and writes an XCCDF `TestResult` XML against the shipped benchmark (`files/U_MS_Windows_Server_2022_STIG_V1R1_Manual-xccdf.xml`, or `STIG_PATH`) to `XML_PATH` (or a temp file) when enabled (for example `ANSIBLE_CALLBACKS_ENABLED=stig_xml`).

Repo playbook: [`windows/compliance.yml`](../../../../../../windows/compliance.yml).

## Requirements

- ansible-core >= 2.16.0
- Target: Windows Server 2022 host reachable over WinRM
- `ansible.windows` collection (`win_regedit`, `win_audit_policy_system`, `win_user_right`, `win_security_policy`, `win_acl`, `win_feature`)

## Role Variables

Defaults live in `defaults/main.yml` (~732 variables). Each of the 198 STIG rules has a `win2022STIG_stigrule_<ID>_Manage` toggle plus rule-specific value variables (registry key/value/type, user lists, etc.); see that file for the complete list. Site-specific rules default to **disabled**, for example:

| Variable | Default | Description |
| --- | --- | --- |
| `win2022STIG_stigrule_254281_Manage` | `false` | DoD-provided NTP server configuration (site-specific placeholder) |
| Various account lockout / password policy rules (`254285`-`254293`) | `false` | Site-specific policy values |

Example of a typical rule pair:

```yaml
win2022STIG_stigrule_254276_Manage: true
win2022STIG_stigrule_254276_SMB1_Key: HKLM:\SYSTEM\CurrentControlSet\Services\mrxsmb10
win2022STIG_stigrule_254276_SMB1_ValueData: 4
win2022STIG_stigrule_254276_SMB1_ValueType: dword
```

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Apply each enabled STIG rule (`win_regedit`, `win_audit_policy_system`, `win_user_right`, `win_security_policy`, `win_acl`, `win_feature`), tagged `stigrule_<ID>`. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.compliance`](../../README.md) for the Windows compliance demos in this repository.

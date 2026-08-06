# demo.compliance.rhel8STIG

Remediate a RHEL 8 host against the DISA STIG for Red Hat Enterprise Linux 8 (`U_RHEL_8_STIG_V2R3`, 171 rules) -- banners, password/crypto policy, package removal, `sysctl`/SELinux hardening, service state, and audit/rsyslog configuration.

```yaml
- name: Run Compliance Profile
  ansible.builtin.include_role:
    name: "demo.compliance.rhel{{ ansible_distribution_major_version }}STIG"
```

Every rule is gated by its own `rhel8STIG_stigrule_<ID>_Manage` boolean (default `true` for all rules) plus companion value variables (`_Value`, `_Line`, `_State`, etc.). Rules are tagged `stigrule_<ID>` for selective runs (`--tags`). Handlers (`dconf_update`, `auditd_restart`, `ssh_restart`, `rsyslog_restart`, `sysctl_load_settings`, `daemon_reload`, `networkmanager_reload`, `logind_restart`, `with_faillock_enable`, `do_reboot`) fire on the relevant config changes.

The role ships a whitelist-required `stig_xml` callback plugin (`callback_plugins/stig_xml.py`) that watches for tasks named `stigrule_<ID>...`, maps `changed` to XCCDF fail / `ok` to pass, and writes an XCCDF `TestResult` XML against the shipped benchmark (`files/U_RHEL_8_STIG_V2R3_Manual-xccdf.xml`, or `STIG_PATH`) to `XML_PATH` (or a temp file) when enabled (for example `ANSIBLE_CALLBACKS_ENABLED=stig_xml`).

Repo playbook: [`linux/disa_stig.yml`](../../../../../../linux/disa_stig.yml) (selects `rhel{{ ansible_distribution_major_version }}STIG` dynamically).

## Requirements

- ansible-core >= 2.16.0
- Target: RHEL 8 host with `become`

## Role Variables

Defaults live in `defaults/main.yml` (~370 variables). Each of the 171 STIG rules has an `rhel8STIG_stigrule_<ID>_Manage` toggle (all default `true`) plus rule-specific value variables; see that file for the complete list.

Example of a typical rule pair:

```yaml
rhel8STIG_stigrule_230239_Manage: true
rhel8STIG_stigrule_230239_krb5_workstation_State: removed

rhel8STIG_stigrule_230240_Manage: true
rhel8STIG_stigrule_230240_SELINUX_Value: enforcing
```

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Apply each enabled STIG rule (`lineinfile`, `yum`, `sysctl`, `ini_file`, `service`, `shell`, `systemd_service`, `copy`), tagged `stigrule_<ID>`; notify the relevant handler on change. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.compliance`](../../README.md) for the Linux compliance demos in this repository.

# demo.compliance.rhel9STIG

Remediate a RHEL 9 host against the DISA STIG for Red Hat Enterprise Linux 9 (`U_RHEL_9_STIG_V2R4`, 286 rules) -- banners, `systemd-journald`/audit configuration, `sysctl` kernel hardening, GRUB/boot file permissions, package removal, and service state. The largest role in the collection.

```yaml
- name: Run Compliance Profile
  ansible.builtin.include_role:
    name: "demo.compliance.rhel{{ ansible_distribution_major_version }}STIG"
```

Every rule is gated by its own `rhel9STIG_stigrule_<ID>_Manage` boolean (default `true` for all rules) plus companion value variables (`_Value`, `_Line`, `_Dest`, `_Content`, etc.). Rules are tagged `stigrule_<ID>` for selective runs (`--tags`). Handlers (`dconf_update`, `auditd_restart`, `ssh_restart`, `rsyslog_restart`, `sysctl_load_settings`, `daemon_reload`, `networkmanager_reload`, `logind_restart`, `with_faillock_enable`, `do_reboot`) fire on the relevant config changes.

The role ships a whitelist-required `stig_xml` callback plugin (`callback_plugins/stig_xml.py`) that watches for tasks named `stigrule_<ID>...`, maps `changed` to XCCDF fail / `ok` to pass, and writes an XCCDF `TestResult` XML against the shipped benchmark (`files/U_RHEL_9_STIG_V2R4_Manual-xccdf.xml`, or `STIG_PATH`) to `XML_PATH` (or a temp file) when enabled (for example `ANSIBLE_CALLBACKS_ENABLED=stig_xml`).

Repo playbook: [`linux/disa_stig.yml`](../../../../../../linux/disa_stig.yml) (selects `rhel{{ ansible_distribution_major_version }}STIG` dynamically).

## Requirements

- ansible-core >= 2.16.0
- Target: RHEL 9 host with `become`

## Role Variables

Defaults live in `defaults/main.yml` (~683 variables). Each of the 286 STIG rules has an `rhel9STIG_stigrule_<ID>_Manage` toggle (all default `true`) plus rule-specific value variables; see that file for the complete list.

Example of a typical rule pair:

```yaml
rhel9STIG_stigrule_257785_Manage: true
rhel9STIG_stigrule_257785_ctrl_alt_del_target_State: masked

rhel9STIG_stigrule_257786_Manage: true
rhel9STIG_stigrule_257786_debug_shell_State: masked
```

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Apply each enabled STIG rule (`lineinfile`, `shell`, `file`, `yum`, `sysctl`, `service`, `ini_file`, `systemd_service`, `copy`), tagged `stigrule_<ID>`; notify the relevant handler on change. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.compliance`](../../README.md) for the Linux compliance demos in this repository.

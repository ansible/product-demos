# demo.compliance.rhel7STIG

Remediate a RHEL 7 host against the DISA STIG for Red Hat Enterprise Linux 7 (`U_RHEL_7_STIG_V3R10`, 144 rules) -- banners, `dconf`/screensaver locks, `sysctl` hardening, package removal, service state, and audit configuration.

```yaml
- name: Run Compliance Profile
  ansible.builtin.include_role:
    name: "demo.compliance.rhel{{ ansible_distribution_major_version }}STIG"
```

Every rule is gated by its own `rhel7STIG_stigrule_<ID>_Manage` boolean (default `true` for all but 2 site-specific rules) plus companion value variables (`_Value`, `_Line`, `_Content`, `_Dest`, etc.). Rules are tagged `stigrule_<ID>` for selective runs (`--tags`). Handlers (`dconf_update`, `auditd_restart`, `ssh_restart`, `do_reboot`) fire on the relevant config changes.

The role ships a whitelist-required `stig_xml` callback plugin (`callback_plugins/stig_xml.py`) that watches for tasks named `stigrule_<ID>...`, maps `changed` to XCCDF fail / `ok` to pass, and writes an XCCDF `TestResult` XML against the shipped benchmark (`files/U_RHEL_7_STIG_V3R10_Manual-xccdf.xml`, or `STIG_PATH`) to `XML_PATH` (or a temp file) when enabled (for example `ANSIBLE_CALLBACKS_ENABLED=stig_xml`).

Repo playbook: [`linux/disa_stig.yml`](../../../../../../linux/disa_stig.yml) (selects `rhel{{ ansible_distribution_major_version }}STIG` dynamically).

## Requirements

- ansible-core >= 2.16.0
- Target: RHEL 7 host with `become`
- `community.general` collection (`ini_file`, and others used by `lineinfile`/`sysctl`/`yum` task equivalents)

## Role Variables

Defaults live in `defaults/main.yml` (~327 variables). Each of the 144 STIG rules has an `rhel7STIG_stigrule_<ID>_Manage` toggle plus rule-specific value variables; see that file for the complete list. Two rules default to **disabled**:

| Variable | Default | Description |
| --- | --- | --- |
| `rhel7STIG_stigrule_204509_Manage` | `false` | Disabled by default (site-specific) |
| `rhel7STIG_stigrule_204624_Manage` | `false` | Disabled by default (site-specific) |

Example of a typical rule pair:

```yaml
rhel7STIG_stigrule_204393_Manage: true
rhel7STIG_stigrule_204393__etc_dconf_db_local_d_01_banner_message_Value: |
  ... DoD warning banner text ...
```

## Entry points

| Entry point | Description |
| --- | --- |
| `main` (default) | Apply each enabled STIG rule (`lineinfile`, `ini_file`, `sysctl`, `yum`, `service`, `shell`, `copy`), tagged `stigrule_<ID>`; notify the relevant handler on change. |

## License

GPL-3.0-or-later

## Authors and Acknowledgments

- Ansible Product Demos -- maintained as part of [`demo.compliance`](../../README.md) for the Linux compliance demos in this repository.

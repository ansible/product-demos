# Reference

The persistent audit watch rule is templated in the `audit_filebeat` role:

`collections/ansible_collections/demo/config_drift/roles/audit_filebeat/templates/sshd-config.rules.j2`

Defaults such as `config_drift_watched_file` and `config_drift_audit_key` control the deployed rule.

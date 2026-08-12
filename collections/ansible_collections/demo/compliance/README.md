# demo.compliance

Local collection containing roles used by the compliance demos in ansible-product-demos ([`linux/disa_stig.yml`](../../../../linux/disa_stig.yml), [`network/compliance.yml`](../../../../network/compliance.yml), [`windows/compliance.yml`](../../../../windows/compliance.yml)).

This collection is not published to Ansible Galaxy or Automation Hub; it exists solely to organize roles used by playbooks in this repository under the `demo.compliance` namespace.

## Contents

### Roles

| Role | Description |
|------|-------------|
| [iosxeSTIG](roles/iosxeSTIG/README.md) | Apply DISA STIG remediation rules to Cisco IOS-XE network devices. |
| [rhel7STIG](roles/rhel7STIG/README.md) | Apply DISA STIG remediation rules to RHEL 7 hosts. |
| [rhel8STIG](roles/rhel8STIG/README.md) | Apply DISA STIG remediation rules to RHEL 8 hosts. |
| [rhel9STIG](roles/rhel9STIG/README.md) | Apply DISA STIG remediation rules to RHEL 9 hosts. |
| [win2022STIG](roles/win2022STIG/README.md) | Apply DISA STIG remediation rules to Windows Server 2022 hosts. |

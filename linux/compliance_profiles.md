# Supported Compliance Profiles

The following compliance profiles are supported by the [**Linux / Enforce Compliance**](README.md#jobs) job template for RHEL 8, RHEL 9, and RHEL 10:

| **Profile** | **Role Repository** |
|-------------|---------------------|
| CIS | https://galaxy.ansible.com/ui/standalone/roles/RedHatOfficial/rhel9_cis/ |
| HIPAA | https://galaxy.ansible.com/ui/standalone/roles/RedHatOfficial/rhel9_hipaa/ |
| OSPP | https://galaxy.ansible.com/ui/standalone/roles/RedHatOfficial/rhel9_ospp/ |
| PCI-DSS | https://galaxy.ansible.com/ui/standalone/roles/RedHatOfficial/rhel9_pci_dss/ |
| DISA STIG | https://galaxy.ansible.com/ui/standalone/roles/RedHatOfficial/rhel9_stig/ |

These roles are derived from the [Compliance as Code](https://github.com/ComplianceAsCode/content) project, which provides SCAP content used by the [OpenSCAP](https://www.open-scap.org/) `oscap` tool.

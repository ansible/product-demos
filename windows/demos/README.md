# Windows Demo Guides

> **Full experience:** Browse the [GitHub Pages demo catalog](https://ipvsean.github.io/product-demos/) for presenter walkthroughs and search/filter.

## Workflows

| Demo | Description | Detail page |
|------|-------------|-------------|
| Setup Active Directory Domain | Full AD setup with DC + domain-joined hosts | [Guide](https://ipvsean.github.io/product-demos/demos/windows-setup-ad-domain/) |

## Standalone jobs

| Demo | Playbook | Description |
|------|----------|-------------|
| Install IIS | [install_iis.yml](../install_iis.yml) | IIS web server with test page |
| Patching | [patching.yml](../patching.yml) | Windows updates by KB/category |
| Rollback | [rollback.yml](../rollback.yml) | Clean up deployments |
| Test Connectivity | [connect.yml](../connect.yml) | Verify WinRM connections |
| Chocolatey Multiple | [windows_choco_multiple.yml](../windows_choco_multiple.yml) | Bulk package install |
| Chocolatey Specific | [windows_choco_specific.yml](../windows_choco_specific.yml) | Single package install |
| Run PowerShell | [powershell.yml](../powershell.yml) | Arbitrary PowerShell |
| Run PowerShell (Kerberos) | [powershell.yml](../powershell.yml) | PowerShell with Kerberos auth |
| Query Services | [powershell_script.yml](../powershell_script.yml) | Service status reporting |
| Password Requirements | [powershell_dsc.yml](../powershell_dsc.yml) | Password policy via DSC |
| AD — Create Domain | [create_ad_domain.yml](../create_ad_domain.yml) | New AD domain |
| AD — Join Domain | [join_ad_domain.yml](../join_ad_domain.yml) | Join existing AD domain |
| AD — New User | [helpdesk_new_user_portal.yml](../helpdesk_new_user_portal.yml) | Helpdesk user creation |
| DISA STIG | [compliance.yml](../compliance.yml) | Windows STIG hardening |

## Quick start

1. Run the **APD | Single demo setup** job template and select `windows`
2. Provision Windows hosts (use **Deploy Cloud Stack in AWS** or add your own)
3. Ensure **APD Machine Credential** has a username and password for WinRM
4. Launch any Windows demo against your provisioned hosts

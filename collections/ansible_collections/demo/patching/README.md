# demo.patching

Local collection containing roles and modules used by the patching demos in ansible-product-demos.

This collection is not published to Ansible Galaxy or Automation Hub; it exists solely to organize roles and modules used by playbooks in this repository under the `demo.patching` namespace.

## Contents

### Roles

| Role | Description |
|------|-------------|
| [build_report_network](roles/build_report_network/README.md) | Install Apache and build an HTML report from network device facts. |
| [build_report_windows](roles/build_report_windows/README.md) | Install Apache and build an HTML report from Windows services and packages facts. |
| [build_report_windows_patch](roles/build_report_windows_patch/README.md) | Install Apache and build an HTML report from Windows update job facts. |
| [patch_linux](roles/patch_linux/README.md) | Upgrade packages via `yum`/`dnf`, then reboot if required. |
| [patch_windows](roles/patch_windows/README.md) | Scan installed packages/services, then apply Windows Updates. |
| [report_linux](roles/report_linux/README.md) | Install Apache and build an HTML report from Linux services and packages facts. |
| [report_linux_patching](roles/report_linux_patching/README.md) | Install Apache and build an HTML report from Linux patching results (yum/dnf). |
| [report_ocp_patching](roles/report_ocp_patching/README.md) | Build an HTML patching report for OpenShift-hosted patching workflows. |
| [report_server](roles/report_server/README.md) | Configure the report landing page and web server (Apache on Linux, IIS on Windows). |
| [report_windows](roles/report_windows/README.md) | Install Apache and build an HTML report from Windows services and packages facts. |
| [report_windows_patching](roles/report_windows_patching/README.md) | Install Apache and build an HTML report from Windows patching job facts. |

### Modules

| Module | Description |
|--------|-------------|
| [scan_packages](plugins/modules/scan_packages.py) | Return installed packages information as fact data. |
| [scan_services](plugins/modules/scan_services.py) | Return service state information as fact data. |
| [win_scan_packages](plugins/modules/win_scan_packages.py) | Return Windows package state information as fact data. |
| [win_scan_services](plugins/modules/win_scan_services.py) | Return Windows service state information as fact data. |

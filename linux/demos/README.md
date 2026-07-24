# Linux Demo Guides

> **Full experience:** Browse the [GitHub Pages demo catalog](https://ipvsean.github.io/product-demos/) for presenter walkthroughs and search/filter.

## Workflows

| Demo | Description | Detail page |
|------|-------------|-------------|
| Compliance Workflow | Scan → inventory → remediate | [Guide](https://ipvsean.github.io/product-demos/demos/linux-compliance-workflow/) |

## Standalone jobs

| Demo | Playbook | Description |
|------|----------|-------------|
| Register with Insights | [ec2_register.yml](../ec2_register.yml) | Register RHEL with Red Hat Insights |
| Troubleshoot | [tshoot.yml](../tshoot.yml) | CPU/memory diagnostics |
| Temporary Sudo | [temp_sudo.yml](../temp_sudo.yml) | Time-limited sudo access |
| Patching | [patching.yml](../patching.yml) | dnf/yum updates with HTML report |
| Start Service | [service_start.yml](../service_start.yml) | Start a systemd service |
| Stop Service | [service_stop.yml](../service_stop.yml) | Stop a systemd service |
| Run Shell Script | [run_script.yml](../run_script.yml) | Execute commands across hosts |
| Fact Scan | [fact_scan.yml](../fact_scan.yml) | Gather facts, packages, services |
| Podman Webserver | [podman.yml](../podman.yml) | Container deployment without K8s |
| System Roles | [system_roles.yml](../system_roles.yml) | RHEL System Roles |
| Install Cockpit | [system_roles.yml](../system_roles.yml) | RHEL Web Console |
| Compliance Enforce | [remediate_out_of_compliance.yml](../remediate_out_of_compliance.yml) | Remediate findings |
| DISA STIG | [disa_stig.yml](../disa_stig.yml) | STIG hardening |
| Multi-profile Compliance | [multi_profile_compliance.yml](../multi_profile_compliance.yml) | CIS/HIPAA/PCI-DSS/STIG |
| Compliance Report | [multi_profile_compliance_report.yml](../multi_profile_compliance_report.yml) | OpenSCAP HTML report |
| Insights Compliance Scan | [insights_compliance_scan.yml](../insights_compliance_scan.yml) | Insights-based scan |
| Deploy Application | [deploy_application.yml](../deploy_application.yml) | Install packages |

## Quick start

1. Run the **APD | Single demo setup** job template and select `linux`
2. Provision RHEL hosts (use **Deploy Cloud Stack in AWS** for cloud-based targets, or add your own)
3. Ensure **APD Machine Credential** has an SSH private key
4. Launch any Linux demo against your provisioned hosts

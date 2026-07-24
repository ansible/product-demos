# Ansible Product Demos — Demo Catalog

> **Tip:** For the best experience, browse the [GitHub Pages site](https://ipvsean.github.io/product-demos/) which has search, filtering, workflow diagrams, and presenter walkthroughs.

## Featured demos

| Demo | Category | Type | Description |
|------|----------|------|-------------|
| [Patch Cloud Stack in AWS](patch-cloud-stack/) | Cloud | Workflow | Snapshot, pre-check, patch, post-check, and compliance report for RHEL + Windows |
| [Deploy Cloud Stack in AWS](deploy-cloud-stack/) | Cloud | Workflow | Provision VPC, keypair, and 5 VMs (2 Windows, 2 RHEL, 1 reports) in one click |

## By category

- [Cloud demos](#cloud) — AWS provisioning, snapshots, patching workflows
- [Linux demos](#linux) — RHEL management, compliance, patching, services
- [Windows demos](#windows) — IIS, AD, patching, PowerShell, Chocolatey
- [Network demos](#network) — Cisco/Palo Alto configuration, reporting, STIG
- [OpenShift demos](#openshift) — CNV virtualization, EDA, Dev Spaces
- [Satellite demos](#satellite) — Content management, compliance, patching

---

### Cloud

| Demo | Type | Description |
|------|------|-------------|
| Deploy Cloud Stack in AWS | Workflow | VPC + keypair + 5 VMs + inventory sync |
| Destroy Cloud Stack in AWS | Workflow | Tear down the full stack |
| Patch Cloud Stack in AWS | Workflow | Enterprise patching with snapshot safety |
| AWS — Create VPC | Playbook | VPC with subnet, security group, route table |
| AWS — Create Keypair | Playbook | EC2 keypair from APD Machine Credential |
| AWS — Create VM | Playbook | EC2 instance from blueprint |
| AWS — Delete VM | Playbook | Terminate EC2 by Name tag |
| AWS — Resize EC2 | Playbook | Change instance type |
| AWS — Snapshot EC2 | Playbook | EBS snapshots for backup |
| AWS — Restore EC2 from Snapshot | Playbook | Volume restore from latest snapshot |
| AWS — Peer Networking | Playbook | VPC peering infrastructure |
| AWS — Transit Networking | Playbook | Transit gateway infrastructure |
| AWS — VPC Report | Playbook | HTML report published to S3 |

### Linux

| Demo | Type | Description |
|------|------|-------------|
| Register with Insights | Playbook | Register RHEL with Red Hat Insights |
| Troubleshoot | Playbook | CPU/memory diagnostics |
| Temporary Sudo | Playbook | Time-limited sudo access |
| Patching | Playbook | dnf/yum updates with HTML report |
| Start Service | Playbook | Start a systemd service |
| Stop Service | Playbook | Stop a systemd service |
| Run Shell Script | Playbook | Execute commands across hosts |
| Fact Scan | Playbook | Gather facts, packages, services |
| Podman Webserver | Playbook | Container deployment without K8s |
| System Roles | Playbook | RHEL System Roles (SELinux, timesync, etc.) |
| Install Web Console (Cockpit) | Playbook | Browser-based system management |
| Compliance Enforce | Playbook | Remediate out-of-compliance systems |
| DISA STIG | Playbook | STIG security hardening |
| Multi-profile Compliance | Playbook | CIS/HIPAA/OSPP/PCI-DSS/STIG enforcement |
| Multi-profile Compliance Report | Playbook | OpenSCAP scan and HTML report |
| Insights Compliance Scan | Playbook | Scan via Insights compliance profiles |
| Deploy Application | Playbook | Install packages on target hosts |
| Compliance Workflow | Workflow | Scan → inventory → remediate |

### Windows

| Demo | Type | Description |
|------|------|-------------|
| Install IIS | Playbook | IIS web server with test page |
| Patching | Playbook | Windows updates by KB/category |
| Rollback | Playbook | Clean up a Windows deployment |
| Test Connectivity | Playbook | Verify WinRM connections |
| Chocolatey Install Multiple | Playbook | Bulk package install |
| Chocolatey Install Specific | Playbook | Single named package install |
| Run PowerShell | Playbook | Arbitrary PowerShell execution |
| Run PowerShell (Kerberos) | Playbook | PowerShell with Kerberos auth |
| Query Services | Playbook | Service status reporting |
| Configure Password Requirements | Playbook | Password policy via DSC |
| AD — Create Domain | Playbook | New Active Directory domain |
| AD — Join Domain | Playbook | Join existing AD domain |
| AD — New User | Playbook | Helpdesk user creation portal |
| DISA STIG | Playbook | Windows STIG hardening |
| Setup Active Directory Domain | Workflow | Full AD setup in AWS |

### Network

| Demo | Type | Description |
|------|------|-------------|
| Golden Configuration | Playbook | ACL/BGP/OSPF/NTP/SNMP config |
| Report | Playbook | Network device facts HTML report |
| DISA STIG | Playbook | Network device compliance |
| Backup | Playbook | Config backup and reporting |
| Palo Alto Firewall Demo | Workflow | Deploy + configure PAN-OS |

### OpenShift

| Demo | Type | Description |
|------|------|-------------|
| EDA — Install Controller | Playbook | Event-Driven Ansible on OCP |
| CNV — Install Operator | Playbook | OpenShift Virtualization operator |
| CNV — Create RHEL VM | Playbook | RHEL VM in CNV |
| CNV — Delete VM | Playbook | Remove CNV VMs |
| Dev Spaces | Playbook | Cloud-based development environments |
| GitLab | Playbook | GitLab on OpenShift |
| CNV — Infra Stack | Workflow | Full CNV infrastructure setup |
| CNV — Patch Workflow | Workflow | Snapshot + patch + restore for CNV VMs |

### Satellite

| Demo | Type | Description |
|------|------|-------------|
| Register with Satellite | Playbook | RHEL registration via activation key |
| Compliance Scan with Satellite | Playbook | OpenSCAP scan reported to Satellite |
| Publish Content View Version | Playbook | New content view version |
| Promote Content View Version | Playbook | Lifecycle environment promotion |
| Patch Dev Workflow | Workflow | Full patching lifecycle with approval gate |

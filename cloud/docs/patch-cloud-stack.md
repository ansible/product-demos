---
layout: demo-detail
demo_slug: patch-cloud-stack
special_thanks: "Joon Paik <jopaik@redhat.com> — original patch demo author"
---

Enterprise-grade patching workflow with snapshot safety, parallel RHEL and Windows paths, automatic restore on failure, and a consolidated HTML compliance report. Based on jopaik/patch_demo, this workflow covers both operating systems in a single execution against the VMs deployed by Deploy Cloud Stack in AWS.

## Prerequisites

- <strong>If using RHDP (demo.redhat.com):</strong> Run <strong>APD | Multi-demo setup</strong> to configure all demo categories at once, or run <strong>APD | Single demo setup</strong> and choose <code>cloud</code> — either option configures the cloud patching templates and credentials. AWS and APD Machine credentials are pre-configured for you.
- <strong>If using your own installation:</strong> Run <strong>APD | Single demo setup</strong> and choose <code>cloud</code>. You will also need to configure the <strong>AWS</strong> credential (Access Key + Secret Key), add an SSH private key and Windows username/password to <strong>APD Machine Credential</strong>, and ensure you have the target VMs, VPC, and keypair provisioned.
- Run <strong>Deploy Cloud Stack in AWS</strong> to create the five target VMs (aws_rhel8, aws_rhel9, aws-dc, aws_win1, reports)
- <strong>RHSM Registration credential:</strong> Fill in your Red Hat org ID and activation key (see credential setup below). <strong>Without this, all RHEL patching steps are skipped</strong> — the workflow still succeeds but only Windows hosts actually get patched. RHEL hosts will show as SKIPPED/UNREGISTERED in the output and compliance report.

## Configure credentials before first run

1. <strong>AWS credential</strong> (pre-configured on demo.redhat.com)<strong>:</strong> Navigate to Resources → Credentials → <code>AWS</code>. Add your AWS Access Key and Secret Key. This is needed for EBS snapshot and restore operations. <em>If you ordered your environment from <a href='https://red.ht/apd-sandbox'>demo.redhat.com</a>, this credential is already configured for you. You only need to set this up if you are running APD on your own installation (homelab, customer site, etc.).</em>
2. <strong>APD Machine Credential</strong> (pre-configured on demo.redhat.com)<strong>:</strong> Navigate to Resources → Credentials → <code>APD Machine Credential</code>. Add an SSH private key (for Linux connections) and set the username/password (for Windows WinRM connections). <em>If you ordered your environment from <a href='https://red.ht/apd-sandbox'>demo.redhat.com</a>, this credential is already configured for you. You only need to set this up if you are running APD on your own installation.</em>
3. <strong>RHSM Registration</strong> (action required for everyone)<strong>:</strong> Navigate to Resources → Credentials → <code>RHSM Registration</code>. This credential was created by the setup job with placeholder values (<code>REPLACEME</code>). Fill in your Red Hat org ID and activation key so RHEL hosts can access advisory repos and get patched. <strong>Without valid RHSM credentials, RHEL patching is completely skipped</strong> — the workflow won't fail, but pre-check, patch, post-check, and rollback all show SKIPPED for RHEL hosts. Only Windows patching proceeds. The compliance report will show RHEL hosts as UNREGISTERED in grey. To find your org ID and create an activation key, visit <a href='https://console.redhat.com/insights/connector/activation-key'>console.redhat.com/insights/connector/activation-key</a>.

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| AWS Region | `aws_region` | multiplechoice | Yes |
| RHEL Advisory IDs | `input_cve_ids` | text | Yes |
| Windows KB IDs | `input_kb_ids` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| Cloud ǀ AWS ǀ Snapshot EC2 | [`cloud/snapshot_ec2.yml`](https://github.com/ansible/product-demos/blob/main/cloud/snapshot_ec2.yml) | Takes EBS snapshots of target EC2 instances |
| Cloud ǀ AWS ǀ Patch Pre-check RHEL | [`cloud/patch_pre_check_rhel.yml`](https://github.com/ansible/product-demos/blob/main/cloud/patch_pre_check_rhel.yml) | Queries dnf for targeted advisory applicability |
| Cloud ǀ AWS ǀ Patch RHEL | [`cloud/patch_rhel.yml`](https://github.com/ansible/product-demos/blob/main/cloud/patch_rhel.yml) | Applies specific RHSA/CVE advisories via dnf |
| Cloud ǀ AWS ǀ Patch Post-check RHEL | [`cloud/patch_post_check_rhel.yml`](https://github.com/ansible/product-demos/blob/main/cloud/patch_post_check_rhel.yml) | Verifies advisories are resolved after patching |
| Cloud ǀ AWS ǀ Patch Pre-check Windows | [`cloud/patch_pre_check_windows.yml`](https://github.com/ansible/product-demos/blob/main/cloud/patch_pre_check_windows.yml) | Queries Windows Update Agent for targeted KB applicability |
| Cloud ǀ AWS ǀ Patch Windows | [`cloud/patch_windows.yml`](https://github.com/ansible/product-demos/blob/main/cloud/patch_windows.yml) | Installs specific KB updates via win_updates |
| Cloud ǀ AWS ǀ Patch Post-check Windows | [`cloud/patch_post_check_windows.yml`](https://github.com/ansible/product-demos/blob/main/cloud/patch_post_check_windows.yml) | Verifies KBs are installed after patching |
| Cloud ǀ AWS ǀ Restore EC2 from Snapshot | [`cloud/restore_ec2.yml`](https://github.com/ansible/product-demos/blob/main/cloud/restore_ec2.yml) | Restores EC2 volumes from latest EBS snapshot |
| Cloud ǀ AWS ǀ Patch Compliance Report | [`cloud/patch_compliance_report.yml`](https://github.com/ansible/product-demos/blob/main/cloud/patch_compliance_report.yml) | Generates HTML compliance dashboard on the reports server |

## Why it matters

- Demonstrates day-2 operations at scale — patching is the number one use case customers ask about
- Parallel RHEL and Windows paths show AAP managing heterogeneous environments in one workflow
- Snapshot-based restore provides a safety net that resonates with change-management audiences
- The HTML compliance report is a tangible artifact you can show stakeholders
- Covers targeted advisory patching (RHSA/CVE for RHEL, KB for Windows), not just "update everything"

## Presenter walkthrough

1. <strong>Run setup:</strong> On RHDP (Red Hat Demo Platform), run <strong>APD | Multi-demo setup</strong> to configure everything. On your own install, run <strong>APD | Single demo setup</strong> → choose <code>cloud</code>. Then fill in the <strong>RHSM Registration</strong> credential with your org ID and activation key (see credential setup above).
2. <strong>Deploy the stack:</strong> Launch <strong>Deploy Cloud Stack in AWS</strong> to create the five target VMs. Wait for it to complete and verify the hosts appear in inventory.
3. <strong>Set the stage:</strong> Show the audience the five VMs in AAP inventory (aws_rhel8, aws_rhel9, aws-dc, aws_win1, reports). Point out it's a mixed Linux/Windows fleet.
4. <strong>Launch the workflow:</strong> Navigate to Templates → Patch Cloud Stack in AWS. Fill in the survey with a real RHSA/CVE and KB (defaults work). Launch.
5. <strong>Snapshot step:</strong> While it runs, explain that the first node takes EBS snapshots of all instances — this is the safety net. 'If anything goes wrong during patching, we restore to this point.'
6. <strong>Parallel paths:</strong> Point out the RHEL and Windows pre-checks running simultaneously. 'One workflow, two operating systems, zero extra effort.'
7. <strong>Pre-check results:</strong> Show the debug output — which advisories are applicable, which hosts are already compliant. 'We check before we change.' <em>Note: If RHSM is not configured, RHEL hosts will show SKIPPED here — this is expected. Without RHSM registration, the hosts can't query Red Hat advisory repos, so all RHEL steps (pre-check, patch, post-check, rollback) are skipped. Windows patching proceeds normally regardless.</em>
8. <strong>Patching:</strong> The patch nodes apply only the targeted advisories. 'We're not running yum update — we're applying specific CVE fixes with an audit trail.'
9. <strong>Post-check / Restore:</strong> Show the success/failure routing. 'If post-check fails, the workflow automatically restores from snapshot. No manual intervention, no 3am pages.'
10. <strong>Compliance report:</strong> Navigate to http://reports/patch_report.html. Walk through the HTML dashboard — status per host, OS badges, missing advisories, reboot needed. Click the advisory count to expand the full list. 'This is the artifact you hand to your auditor or change board.'<br><br><img src='/product-demos/assets/img/patch-compliance-report.png' alt='Patch Compliance Dashboard screenshot' style='max-width: 100%; border: 1px solid #1a3322; border-radius: 8px; margin-top: 8px;'>

## Talking points

- This is a real-world patching workflow — not a hello-world demo. It mirrors what enterprises actually deploy with AAP.
- The parallel RHEL/Windows paths highlight AAP's ability to manage heterogeneous environments without separate tools.
- Snapshot-before-patch is a pattern customers love — it eliminates the fear of patching production systems.
- Targeted advisory patching (specific CVEs/KBs) versus blanket updates shows precision and auditability.
- The compliance report generates automatically — no separate CMDB integration needed for a quick compliance view.
- Unregistered RHEL hosts are handled gracefully — they show as SKIPPED, not as failures. If someone configures the RHSM credential, they auto-register.

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Cloud Stack in AWS](/product-demos/demos/deploy-cloud-stack/) | Required prerequisite; creates the five target VMs |
| 🐧 [Patching](/product-demos/demos/linux-patching/) | Standalone Linux patching job (simpler, no workflow) |
| 🐧 [Register with Insights](/product-demos/demos/linux-register-insights/) | Register RHEL hosts with RHSM for full advisory access |

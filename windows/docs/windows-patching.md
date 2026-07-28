---
layout: demo-detail
demo_slug: windows-patching
---

Apply Windows updates by category to Windows Server hosts and generate an HTML patch report. The playbook uses the demo.patching.patch_windows role to install updates filtered by category (Security, Critical, Feature Packs, etc.), with optional reboot control. A report server is deployed automatically to publish patching results. Runs in check mode by default.

## Prerequisites

- Windows hosts in the <strong>Ansible Product Demos Inventory</strong> (deployed by <strong>Deploy Cloud Stack in AWS</strong>)
- WinRM connectivity via <strong>APD Machine Credential</strong>
- A Windows report server (<code>aws_win1</code>) in the <code>os_windows</code> inventory group

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | No |
| Update categories | `win_update_categories` | multiselect | No |
| Reboot after install? | `allow_reboot` | multiplechoice | No |

## Why it matters

- Windows patching is a top customer pain point — this demo proves AAP handles it natively
- Category-based filtering (SecurityUpdates, CriticalUpdates, etc.) shows precision control over what gets installed
- Check mode lets you preview updates before applying — critical for change management approval
- The HTML report provides audit evidence without relying on WSUS or SCCM reporting
- Reboot control via survey shows operational safety for production Windows servers

## Presenter walkthrough

1. <strong>Show the survey:</strong> Walk through the category selector. 'We can target just security updates, or cast a wider net. The operator chooses — not the tool.'
2. <strong>Launch in check mode:</strong> Run against the Windows hosts. 'Check mode queries Windows Update Agent without installing anything. We see exactly what would change.'
3. <strong>Review the output:</strong> Show which KBs are applicable per host. Point out the reboot-required indicators.
4. <strong>Switch to run mode:</strong> Re-launch with job type set to Run. Highlight the reboot control option. 'In production, you might patch during a maintenance window and defer reboots.'
5. <strong>Show the report:</strong> Navigate to the report server and walk through the HTML patching report.
6. <strong>Connect to the bigger picture:</strong> 'For environments with both Windows and RHEL, our Patch Cloud Stack workflow handles both in parallel with EBS snapshot rollback.'

## Talking points

- Ansible manages Windows natively through WinRM — no agent installation required on the target hosts.
- Category filtering means you can apply just security updates during an emergency patch cycle without pulling in feature packs.
- Check mode is your dry run. Show the change board exactly what will happen before you touch production.
- The reboot survey option is a small detail that matters in production — operators control when reboots happen, not the automation.
- This same patching pattern works on-prem, in AWS, or in Azure. The playbook does not care where the Windows host lives.

## Related demos

| Demo | Description |
|------|-------------|
| 🩹 [Patch Cloud Stack in AWS](/product-demos/demos/patch-cloud-stack/) | Full workflow with EBS snapshots, parallel RHEL and Windows patching, and automatic rollback |
| 🪟 [Install IIS](/product-demos/demos/windows-install-iis/) | Quick Windows demo to show application deployment alongside patching |
| 🪟 [Setup Active Directory Domain](/product-demos/demos/windows-setup-ad-domain/) | Provision a full AD environment to demonstrate domain-joined Windows patching |

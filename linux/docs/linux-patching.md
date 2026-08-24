# Patching


Apply security updates to RHEL servers and generate an HTML patch report. The playbook installs yum-utils, applies patches via the demo.patching.patch_linux role, optionally triggers an Insights Client scan, and publishes a patching compliance report to a dedicated report server. Runs in check mode by default so you can audit before applying.

## Prerequisites

- Linux hosts in the **Ansible Product Demos Inventory**
- SSH connectivity via **APD Machine Credential**
- A host named `reports` in inventory to receive the HTML report (deployed by **Deploy Cloud Stack in AWS**)
- (Optional) Insights Client configured on target hosts for post-patch scanning

## Survey prompts

| Prompt | Variable | Type | Required |
|--------|----------|------|----------|
| Server Name or Pattern | `_hosts` | text | Yes |

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| LINUX ǀ Patching | [`linux/patching.yml`](../patching.yml) | Apply security updates, optionally scan with Insights Client, and publish an HTML patch report |

## Why it matters

- Patching is the number one use case customers ask about — this demo addresses it directly
- Check mode lets you show a safe audit-first workflow before committing changes
- The HTML report gives stakeholders a tangible artifact without a separate CMDB integration
- Insights Client integration shows how AAP and Red Hat Insights work together for visibility
- Demonstrates role-based content reuse with the demo.patching collection

## Presenter walkthrough

1. **Explain check mode:** Show the audience that this template defaults to check mode. 'We can audit what would change before we touch a single package.'
2. **Launch in check mode:** Run against a group of RHEL hosts. Walk through the output — which packages would be updated, which hosts are already current.
3. **Switch to run mode:** Re-launch the job and change the job type to Run. 'Now we apply the patches for real — same playbook, same survey, different intent.'
4. **Show the report:** Navigate to the reports server and open the patching report. Walk through the per-host breakdown of applied updates.
5. **Insights integration:** If Insights Client is configured, show how the post-patch scan updates the host profile in Red Hat Insights automatically.
6. **Connect to the bigger picture:** 'For a full enterprise workflow with snapshots and rollback, check out Patch Cloud Stack in AWS.'

## Talking points

- Check mode versus run mode is a powerful pattern — audit first, patch second, all from the same template.
- The HTML report is generated automatically on every run. Hand it to your change board or attach it to a ticket.
- Insights Client scanning after patching closes the loop — your compliance dashboard updates in near real-time.
- This is a single job template. For heterogeneous environments with Windows, snapshots, and rollback, we have a full workflow demo.

## Related demos

| Demo | Description |
|------|-------------|
| 🩹 [Patch Cloud Stack in AWS](../../cloud/docs/patch-cloud-stack.md) | Full enterprise patching workflow with snapshots, parallel RHEL/Windows paths, and automatic rollback |
| 🐧 [Register with Insights](./linux-register-insights.md) | Register hosts with Red Hat Insights for advisory visibility and dynamic inventory |
| 🐧 [Multi-profile Compliance](./linux-multi-profile-compliance.md) | Run an OpenSCAP report to assess security posture before and after patching |

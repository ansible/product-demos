# Staging and Upgrade

Performs a two-phase Cisco IOS-XE software upgrade on the containerlab Catalyst 8000V (`cat8kv1`). This is the usual workflow for production network upgrades. **Staging** copies the new image to the router's bootflash and verifies its integrity during normal operations. **Upgrade** installs and activates the staged image in a maintenance window, waits for the router to reload, and confirms that it is running the new version.

The lab boots `cat8kv1` on IOS-XE 17.13.01a. The demo upgrades it to 17.15.01a.

## Prerequisites

- Containerlab stack deployed via the **NETWORK ǀ Deploy Containerlab Stack** workflow. The topology includes the `scp-server` node at `172.20.20.11` that hosts the IOS-XE image.
- **Containerlab Device Access** credential configured
- **SCP Credential** configured (created by Network setup with the `scpuser` account that the `scp-server` node creates)
- ContainerLab Inventory synced with hypervisor IP

Run **NETWORK ǀ Backup** before upgrading so you have a copy of the running configuration. If either job times out waiting for device SSH, run **NETWORK ǀ Containerlab ǀ Troubleshoot** first.

## Job templates

| Template | Playbook | Description |
|----------|----------|-------------|
| NETWORK ǀ Staging | [`network/staging.yml`](../staging.yml) | Copies the selected IOS-XE image from the SCP server to bootflash and verifies its SHA512 hash |
| NETWORK ǀ Upgrade | [`network/upgrade.yml`](../upgrade.yml) | Installs and activates the staged image, waits for the reload, and confirms the new version |

Both templates run against the `clab_ios` group by default. Set `_hosts` to target different devices. Each template has a survey that asks for the IOS-XE version (`image_staging` or `image_upgrade`). The image filename is derived from the version: `c8000v-universalk9.<version>.SPA.bin`.

## Demo flow

1. Run **NETWORK ǀ Staging** and select `17.15.01a`.
2. Run **NETWORK ǀ Upgrade** and select the same version.
3. Optionally, run **NETWORK ǀ Report** to show the new software version in the device report.

Staging must finish successfully before Upgrade. Upgrade fails immediately if the image is not in bootflash.

### Phase 1: Staging

`network/staging.yml` prepares the router without disrupting traffic:

1. **Record the current version.** Runs `show version` and prints the first line, so the job output shows the starting release.
2. **Prepare the router for SCP.** Enables `ip scp server enable` and raises the SSH and TCP window sizes to `131072` to speed up the large image transfer.
3. **Check whether the image is already staged.** Runs `dir bootflash: | include <image>`. If the file is already present, the transfer is skipped, so you can rerun Staging safely.
4. **Pull the image to the router.** Runs `copy scp: flash: vrf clab-mgmt` and answers the interactive prompts for the server, username, source and destination filenames, and password. The router pulls the image from `scp-server` over the management VRF. The SCP server address comes from the template's `scp_server` extra var; the username and password are injected by the **SCP Credential**. The command timeout is set to 20 minutes for the transfer.
5. **Verify image integrity.** Runs `verify /sha512 bootflash:/<image> <hash>` against the expected hash in the template's `sha_hash` extra var. This check runs even if the transfer was skipped, so an existing file is still validated. If the router does not report `Verified`, the job fails with `SHA512 Hash Check Fails. Please check the uploaded image!`.

When Staging succeeds, the router is still running the original version, and a verified image is in bootflash ready to install.

### Phase 2: Upgrade

`network/upgrade.yml` performs the disruptive change and verifies the result. It has two plays.

**Upgrade Router IOS Image**

1. **Set the boot variable.** Removes existing `boot system` statements, adds `boot system bootflash:packages.conf` for install mode, and saves the configuration.
2. **Confirm the image is staged.** Checks bootflash for the image and fails the job if it is missing.
3. **Install, activate, and commit.** Runs `install add file bootflash:<image> activate commit` and answers `y` to the reload prompt. This single command adds the package, activates it (which reloads the router), and commits it so the new version persists across later reloads. The command timeout is 20 minutes.
4. **Wait for the reload.** If the install output does not contain `No Change`, the job waits 60 seconds, then polls the router's SSH port for up to 550 seconds. It then retries `show version` up to 10 times, 30 seconds apart, until IOS-XE accepts commands. If the router is already on the target version, it doesn't reload, so these waits are skipped.

**Confirm Bootloader After Reload**

5. **Verify the running version.** Runs `show version` again and asserts that the target version is present. The job reports `<version> is present` on success and fails with `<version> is not present` otherwise.

## Talking points

- **Separate staging from the maintenance window.** Copying and verifying a large image is slow but not disruptive, so it can run during business hours. Only the Upgrade job causes downtime.
- **Built-in safety checks.** The SHA512 verification, the bootflash check before install, and the version assertion after reload each stop the workflow before a bad image or failed upgrade goes unnoticed.
- **Safe to rerun.** Staging skips an image that is already present. Upgrade detects `No Change` and skips the reload wait when the router is already on the target release.
- **Automates interactive CLI.** `ansible.netcommon.cli_command` and `cisco.ios.ios_command` answer the interactive `copy` and `install` prompts that would otherwise need someone at a console.
- **Credentials stay out of the playbook.** SCP credentials come from a custom AAP credential type rather than survey answers or hard-coded vars.

## Adding a new IOS-XE version

The surveys offer only `17.15.01a`, and the template's `sha_hash` extra var matches that image. To offer another release:

1. Make the `c8000v-universalk9.<version>.SPA.bin` file available on the `scp-server` node.
2. Add the version to the survey choices for both templates in [`network/setup.yml`](../setup.yml).
3. Update the Staging template's `sha_hash` to the SHA512 hash published by Cisco for that image.

## Related demos

| Demo | Description |
|------|-------------|
| 🚀 [Deploy Containerlab Stack](./network-deploy-containerlab-stack.md) | Provision the lab, including the SCP server, before staging an image |
| 🌐 [Backup](./network-backup.md) | Back up the running configuration before upgrading |
| 🌐 [Report](./network-report.md) | Confirm the new software version after the upgrade |
| 🛠️ [Troubleshoot Containerlab](./network-troubleshoot-containerlab.md) | Diagnose device SSH or container issues if a job times out |

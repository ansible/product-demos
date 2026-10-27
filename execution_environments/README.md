# Execution Environment Images for Ansible Product Demos

When the Ansible Product Demos setup job template is run, it creates a number of execution environment definitions on the automation controller.  The content of this directory is used to create and update the default APD execution environment images defined during the setup process, [quay.io/ansible-product-demos/apd-ee-26](quay.io/ansible-product-demos/apd-ee-26).

Currently the execution environment image is created manually using the `build.sh` script, with a future goal of building in a CI pipeline when the EE definition or requirements are updated.

## Building the execution environment images

1. `podman login registry.redhat.io` in order to pull the base EE images
2. `export ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN="<token>"` obtained from [Automation Hub](https://console.redhat.com/ansible/automation-hub/token)
3. `export ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN="<token>"` (same token as above)
4. `./build.sh` to build the EE image

The `build.sh` script creates a multi-architecture EE image for the amd64 (x86_64) and arm64 (aarch64) platforms.  It does so by creating the build context using `ansible-builder create`, then creating a podman manifest definition and building an EE image for each supported platform.

NOTE: Podman will use qemu to emulate the non-native architecture at build time, so the build must be performed on a system which includes the qemu-user-static package.  Builds have only been tested on MacOS using podman-desktop with the native Fedora-based podman machine.

## Network demo testing prerequisite

The official Product Demos EE must be rebuilt and published with the updated
EE definitions and requirements in this PR before testing the multi-vendor
configuration and report jobs. Updating or syncing the APD project does not
update an already published EE image.

The jobs require the pinned `ansible.netcommon`, `cisco.ios`, `cisco.nxos`,
`arista.eos`, and `juniper.device` collections, plus `ncclient` and `passlib`.
Build the EE for the target AAP version, publish it to an accessible registry,
and select that image for Product Demos EE before running Network setup and
the demo jobs. Attach a Container Registry credential when using a private
registry. Live acceptance was performed with a rebuilt AAP 2.7 EE on x86_64.

## AAP 2.7 compatibility

The pinned AAP 2.7 base image ships Ansible core 2.16. The non-network
requirements retain their original minimums and add compatibility ceilings,
rather than pinning cloud, Linux, and Windows content to individual releases:

| Collection | Allowed versions | Version in the tested rebuilt EE |
|---|---|---|
| `amazon.aws` | `>=7.5.0,<10.0.0` | 9.5.2 |
| `community.aws` | `>=7.0.0,<10.0.0` | 9.3.0 |
| `community.general` | `>=8.0.0,<12.0.0` | 11.4.9 |
| `chocolatey.chocolatey` | `>=1.5.1,<1.6.0` | 1.5.3 |

These bounds affect the entire AAP 2.7 EE. They are required by the base runtime:
[`amazon.aws` 10](https://github.com/ansible-collections/amazon.aws/blob/10.0.0/meta/runtime.yml),
[`community.aws` 10](https://github.com/ansible-collections/community.aws/blob/10.0.0/meta/runtime.yml),
and [`community.general` 12](https://github.com/ansible-collections/community.general/blob/12.0.0/meta/runtime.yml)
require core 2.17 or newer. [Chocolatey 1.6](https://github.com/chocolatey-community/chocolatey-ansible/blob/1.6.0/chocolatey/meta/runtime.yml)
requires core 2.18 or newer.
`community.aws` 9.3.0 additionally depends on `amazon.aws` below 10.

Network acceptance exercised AWS provisioning and the Linux filesystem,
SELinux, and report-hosting tasks using the versions listed above. This is not
a full regression run of the cloud, Windows, or Linux demo catalogs; Windows
package management and the other demo workflows need their own live validation
before claiming EE-wide demo coverage. The network collections remain pinned
to the versions selected for the multi-vendor report. Check collection
`meta/runtime.yml` requirements and dependencies against the base runtime when
refreshing these bounds or pins.

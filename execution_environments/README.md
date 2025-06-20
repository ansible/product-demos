# Execution Environment Images for Ansible Product Demos

When the Ansible Product Demos setup job template is run, it creates a number of execution environment definitions on the automation controller.  The content of this directory is used to create and update the default APD execution environment images defined during the setup process, [quay.io/ansible-product-demos/apd-ee-25](quay.io/ansible-product-demos/apd-ee-25).

Currently the execution environment image is created manually using the `build.sh` script, with a future goal of building in a CI pipeline when the EE definition or requirements are updated.

## Building the execution environment images

1. `podman login registry.redhat.io` in order to pull the base EE images
2. `export ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN="<token>"` obtained from [Automation Hub](https://console.redhat.com/ansible/automation-hub/token)
3. `export ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN="<token>"` (same token as above)
4. `./build.sh` to build the EE image

The `build.sh` script creates a multi-architecture EE image for the amd64 (x86_64) and arm64 (aarch64) platforms.  It does so by creating the build context using `ansible-builder create`, then creating a podman manifest definition and building an EE image for each supported platform.

NOTE: Podman will use qemu to emulate the non-native architecture at build time, so the build must be performed on a system which includes the qemu-user-static package.  Builds have only been tested on MacOS using podman-desktop with the native Fedora-based podman machine.

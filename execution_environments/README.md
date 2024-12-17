# Execution Environment Images for Ansible Product Demos

When the Ansible Product Demos setup job template is run, it creates a number of execution environment definitions on the automation controller.  The content of this directory is used to create and update the default execution environment images defined during the setup process.

Currently these execution environment images are created manually using the `build.sh` script, with a future goal of building in a CI pipeline when any EE definitions or requirements are updated.

## Building the execution environment images

1. `podman login registry.redhat.io` in order to pull the base EE images
2. `export ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN="<token>"` obtained from [Automation Hub](https://console.redhat.com/ansible/automation-hub/token)
3. `export ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN="<token>"` (same as above)
4. `./build.sh` to build the EE images and add them to your local podman image cache

The `build.sh` script creates multiple EE images, each based on the ee-minimal image that comes with a different minor version of AAP.  These images are created in the "quay.io/ansible-product-demos" namespace.  Currently the script builds the following images:

* quay.io/ansible-product-demos/apd-ee-24
* quay.io/ansible-product-demos/apd-ee-25

# Execution Environment Images for Ansible Product Demos

When the Ansible Product Demos setup job template is run, it creates a number of execution environment definitions on the automation controller.  The content of this directory is used to create and update the default execution environment images defined during the setup process.

Currently these execution environment images are created manually using the `build.sh` script, with a future goal of building in a CI pipeline when any EE definitions or requirements are updated.

## Building the execution environment images

1. Download the [openshift-clients rpm](https://access.redhat.com/downloads/content/rhel---9/x86_64/20821/openshift-clients/4.16.0-202408021139.p0.ge8fb3c0.assembly.stream.el9/x86_64/fd431d51/package)
2. Overwrite existing link to git-lfs by copying downloaded RPM to `<repo-root>/execution-environments/openshift-clients-4.16.0-202408021139.p0.ge8fb3c0.assembly.stream.el9.x86_64.rpm`
3. `podman login registry.redhat.io` in order to pull the base EE images
4. `export ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN="<token>"` obtained from [Automation Hub](https://console.redhat.com/ansible/automation-hub/token)
5. `export ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN="<token>"` (same as above)
6. `./build.sh` to build the EE images and add them to your local podman image cache

The `build.sh` script creates multiple EE images, each based on the ee-minimal image that comes with a different minor version of AAP.  These images are created in the "quay.io/ansible-product-demos" namespace.  Currently the script builds the following images:

* quay.io/ansible-product-demos/apd-ee-24
* quay.io/ansible-product-demos/apd-ee-25

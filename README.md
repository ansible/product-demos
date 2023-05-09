# Official Ansible Product Demos

This is a centralized location for Ansible Product Demos. This project is a collection of use cases implemented with Ansible for use with the Ansible Automation Platform.

| Demo Name | Description |
|-----------|-------------|
| [Linux](linux/README.md) | Repository of demos for RHEL and Linux automation |
| [Windows](windows/README.md) | Repository of demos for Windows Server automation |
| [Cloud](cloud/README.md) | Demo for infrastructure and cloud provisioning automation |
| [Network](network/README.md) | Ansible Network automation demos |
| [Satellite](satellite/README.md) | Demos of automation with Red Hat Satellite Server |

## Contributions

If you would like to contribute to this project please refer to [contribution guide](CONTRIBUTING.md) for best practices.

## Using this project

  > This project is tested for compatibility with the [red.ht/aap-product-demos](red.ht/aap-product-demos) lab environment. To use with other Ansible Controller installations, review the [pre-requisite documentation](https://github.com/RedHatGov/ansible-tower-samples/tree/product-demos).

1. First you must create a credential for [Automation Hub](https://console.redhat.com/ansible/automation-hub/) to successfully sync collections used by this project.
   
   1. In the Credentials section of the Controller UI, add a new Credential called `Automation Hub` with the type `Ansible Galaxy/Automation Hub API Token`
   2. You can obtain a token [here](https://console.redhat.com/ansible/automation-hub/token). This page will also provide the Server URL and Auth Server URL.
   3. Next, click on Organizations and edit the `Default` organization. Add your `Automation Hub` credential to the `Galaxy Credentials` section. Don't forget to click **Save**!!

      > You can also use an execution environment for disconnected environments. To do this, you must disable collection downloads in the Controller. This can be done in `Settings` > `Job Settings`. This setting prevents the controller from downloading collections listed in the [collections/requirements.yml](collections/requirements.yml) file.

2. If it has not been created for you, add a Project called `Ansible official demo project` with this repo as a source. NOTE: if you are using a fork, be sure that you have the correct URL. Update the project.

3. Finally, Create a Job Template called `Setup` with the following configuration:
  
     - Name: Setup
     - Inventory: Workshop Inventory
     - Exec Env: Control Plane EE
     - Playbook: setup_demo.yml
     - Credentials:
        - Type: Red Hat Ansible Automation Platform
        - Name: Controller Credential
     - Extra vars:

            demo: <linux or windows or cloud or network>

## Bring Your Own Demo

Can't find what you're looking for? Customize this repo to make it your own.

1. Create a fork of this repo.
2. Update the URL of the `Ansible official demo project` in the Controller.
3. Make changes as needed and run the **Setup** job

See the [contribution guide](CONTRIBUTING.md) for more details on how to customize the project.

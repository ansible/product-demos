[![Lab](https://img.shields.io/badge/Try%20Me-EE0000?style=for-the-badge&logo=redhat&logoColor=white)](https://red.ht/aap-product-demos)
[![Dev Spaces](https://img.shields.io/badge/Customize%20Here-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://workspaces.openshift.com/f?url=https://github.com/ansible/product-demos)

# Official Ansible Product Demos

This is a centralized location for all Ansible Product Demos going forward. 

| Demo Name | Description |
|-----------|-------------|
| [Linux](linux/README.md) | Repository of demos for RHEL and Linux automation |
| [Windows](windows/README.md) | Repository of demos for Windows Server automation |
| [Cloud](cloud/README.md) | Demo for infrastructure and cloud provisioning automation |
| [Network](network/README.md) | Ansible Network automation demos |

## Contributions

If you would like to contribute to this project please refer to [contribution guide](CONTRIBUTING.md) for best practices.

## Using this project

  > This project is tested for compatibility with AAP2 Linux Automation Workshop available to Red Hat Employees and Partners. To use with other Ansible Controller installations, review the [pre-requisite documentation](https://github.com/RedHatGov/ansible-tower-samples/tree/product-demos).

1. First you must create a credential for [Automation Hub](https://console.redhat.com/ansible/automation-hub/) to successfully sync collections used by this project.
   
   1. In the Credentials section of the Controller UI, add a new Credential called `Automation Hub` with the type `Ansible Galaxy/Automation Hub API Token`
   2. You can obtain a token [here](https://console.redhat.com/ansible/automation-hub/token). This page will also provide the Server URL and Auth Server URL.
   3. Next, click on Organizations and edit the `Default` organization. Add your `Automation Hub` credential to the `Galaxy Credentials` section. Don't forget to click Save!!

2. If it has not been created for you, add a Project called `Ansible official demo project` with this repo as a source. NOTE: if you are using a fork, be sure that you have the correct URL. Update the project.
3. Finally, Create a Job Template called `Setup` with the following configuration:
  
     - Name: Setup
     - Inventory: Demo Inventory
     - Exec Env: Control Plane EE
     - Playbook: setup_demo.yml
     - Credentials:

        - Type: Red Hat Ansible Automation Platform
        - Name: Controller Credential
     - Extra vars:
  
            demo: <linux or windows or cloud or network>

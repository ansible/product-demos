# Official Ansible Product Demos

This is a centralized location for all Ansible Product Demos going forward. 

| Demo Name                                                        | Description                                                                                 |
|------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| [AAP on CodeReady](aap-on-crc/README.md)                         | Repository and video of how to install Ansible Automation Platform on Code Ready Containers |
| [Infrastructure Demos](old-demo-repository#infrastructure-demos) | Azure, AWS, Chocolatey, Linux and Windows Demos                                             |
| [Network Demos](old-demo-repository#network-demos)               | Cisco IOS and F5 Demos                                                                      |
| [Security Demos](old-demo-repository#security-demos)             | OSCAP and hardening demos                                                                   |
| [Developer Demos](old-demo-repository#developer-demos)           | Create Reports with Ansible                                                                 |

## Contributions

Please push contributions via a pull request following the naming convention of name-of-demo.

[![GitHub Super-Linter](https://github.com/ansible/ansible-demos/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)


## Using this project

1. First you must create a credential to access Automation Hub to load the collections used by this project.
   
   1. In the Credentials section of the Controller UI, add a new Credential called `Automation Hub` with the type `Ansible Galaxy/Automation Hub API Token`
   2. You can obtain a token [here](https://console.redhat.com/ansible/automation-hub/token). This page will also provide the Server URL and Auth Server URL.
   3. Next, click on Organizations and edit the `Default` organization. Add your `Automation Hub` credential to the `Galaxy Credentials` section.

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
  
            demo: <linux or windows>

4. If you require a Windows Active Directory domain you will need to run the "ACTIVE DIRECTORY / Create Active Directory domain" template after the Windows setup completes. This will create the "ansible.local" domain as well as a few generic users and groups.
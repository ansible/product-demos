# Network Demos

## Table of Contents
- [Network Demos](#network-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
    - [Project](#project)
    - [Inventory](#inventory)
  - [Suggested Usage](#suggested-usage)

## About These Demos
This category of demos shows examples of network operations and management with Ansible Automation Platform. The list of demos can be found below. See the [Suggested Usage](#suggested-usage) section of this document for recommendations on how to best use these demos.
- [**NETWORK / Configuration**](https://github.com/nleiva/ansible-net-modules/blob/main/main.yml) - Deploy golden configurations for different resources to Cisco IOS, IOSXR, and NXOS.

### Project

These demos leverage playbooks from a [git repo](https://github.com/nleiva/ansible-net-modules) that is added as the **`Network Golden Configs`** Project in your Ansible Controller. Review this repo for the playbooks to configure different resources and network config templates that will be configured.

### Inventory

These demos leverage "always-on" instances for Cisco IOS, IOSXR, and NXOS from [Cisco DevNet Sandboxes](https://developer.cisco.com/docs/sandbox/#!getting-started/always-on-sandboxes). These instances are shared and do not provide admin access but they are instantly avaible all the time meaning not setup time is required.

A **`Network Inventory`** is created when setting up these demos and a dynamic source is added to populate the Always-On instances. Review the inventory file [here](https://github.com/nleiva/ansible-net-modules/blob/main/hosts).

## Suggested Usage

**NETWORK / Configuration** - Use this job to execute different [Ansible Network Resource Modules](https://docs.ansible.com/ansible/latest/network/user_guide/network_resource_modules.html) to deploy golden configs. Below is a list of the different resources the can be configured with a link to their golden config.
  - [acls](https://github.com/nleiva/ansible-net-modules/blob/main/acls.cfg)
  - [banner](https://github.com/nleiva/ansible-net-modules/blob/main/banner.cfg)
  - [bgp_global](https://github.com/nleiva/ansible-net-modules/blob/main/bgp_global.cfg)
  - [hostname](https://github.com/nleiva/ansible-net-modules/blob/main/hostname.cfg)
  - [l3_interface](https://github.com/nleiva/ansible-net-modules/blob/main/l3_interface.cfg)
  - [logging](https://github.com/nleiva/ansible-net-modules/blob/main/logging.cfg)
  - [ntp](https://github.com/nleiva/ansible-net-modules/blob/main/ntp.cfg)
  - [ospfv2](https://github.com/nleiva/ansible-net-modules/blob/main/ospfv2.cfg)
  - [prefix_lists](https://github.com/nleiva/ansible-net-modules/blob/main/prefix_lists.cfg)
  - [snmp](https://github.com/nleiva/ansible-net-modules/blob/main/snmp.cfg)
  - [user](https://github.com/nleiva/ansible-net-modules/blob/main/user.cfg)

### NETWORK /Router Backups**
Use the following job-templates (Deploy Gitea, and Backups to Gitea ) to backup the router and switch configs to Gitea 

**NETWORK / Deploy Gitea** Run this job-template first to deploy a Gitea container on node1.
Note, only run this job-template once or you will observe ignored-errors for the existing user and repo.  

This job-template will use the gitea.yml playbook to complete the following tasks on node1:
- Prompts the user to create a simple password for Gitea (no special characters)
- Installs Podman 
- Runs the gitea container
- Installs gitea with the admin user "gitea"
- Creates a repo called "backups"

**NETWORK / Backups to Gitea** - Run this job-template (Backups to Gitea) to backup the network device configurations to a Gitea repository.
Note, the survey prompts for the gitea password created in the "Deploy Gitea" job-template!

***Upon completing the above job-template, the demo requires the use of the vscode tab in to validate***

#### From the VS Code terminal ####
- Clone the "backups" repo from Gitea after running the "NETWORK / Backups to Gitea" Job-template
```
[rhel@control ansible-files]$ git clone http://node1:3000/gitea/backups.git
Cloning into 'backups'...
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 5 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (5/5), 7.78 KiB | 7.78 MiB/s, done.
```
- To see the backups change directories into "backups" and list the files
```
rhel@control ansible-files]$ cd backups/
[rhel@control backups]$ ls
sandbox-iosxe-latest-1.cisco.com_config.2023-08-03@19:10:13  sandbox-nxos-1.cisco.com_config.2023-08-03@19:10:34
sandbox-iosxr-1.cisco.com_config.2023-08-03@19:10:19
```
- Cat the files
```
[rhel@control backups]$ cat sandbox-iosxe-latest-1.cisco.com_config.2023-08-03\@19\:10\:13 
Building configuration...

Current configuration : 7167 bytes
!
! Last configuration change at 18:58:48 UTC Thu Aug 3 2023 by admin
!
version 17.9
service timestamps debug datetime msec
service timestamps log datetime msec
service call-home
platform qfp utilization monitor load 80
platform punt-keepalive disable-kernel-core
platform console virtual
!
hostname Cat8000V
!
``` 
#### What if you Run it again? ####
If you run the "Backups to Gitea" again it will create a new branch that includes the original and new backup files.
Note, It's possible to merge these with the main branch, if needed.

- To see the new branch run the following 'similar' commands
```
 [rhel@control backups]$ git pull
remote: Enumerating objects: 4, done.
remote: Counting objects: 100% (4/4), done.
remote: Compressing objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (3/3), 2.52 KiB | 2.52 MiB/s, done.
From http://node1:3000/gitea/backups
 * [new branch]      ansible-backup_cisco_configs_to_gitea-2023-08-03T192936.882436+0000 -> origin/ansible-backup_cisco_configs_to_gitea-2023-08-03T192936.882436+0000
Already up to date.
[rhel@control backups]$ git checkout ansible-backup_cisco_configs_to_gitea-2023-08-03T192936.882436+0000
Branch 'ansible-backup_cisco_configs_to_gitea-2023-08-03T192936.882436+0000' set up to track remote branch 'ansible-backup_cisco_configs_to_gitea-2023-08-03T192936.882436+0000' from 'origin'.
Switched to a new branch 'ansible-backup_cisco_configs_to_gitea-2023-08-03T192936.882436+0000'
[rhel@control backups]$ ls
sandbox-iosxe-latest-1.cisco.com_config.2023-08-03@19:10:13  sandbox-iosxr-1.cisco.com_config.2023-08-03@19:29:48
sandbox-iosxe-latest-1.cisco.com_config.2023-08-03@19:29:41  sandbox-nxos-1.cisco.com_config.2023-08-03@19:10:34
sandbox-iosxr-1.cisco.com_config.2023-08-03@19:10:19         sandbox-nxos-1.cisco.com_config.2023-08-03@19:29:57
```



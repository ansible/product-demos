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

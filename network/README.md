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

To run the demos, deploy them using Infrastructure as Code, run either the "Product Demos | Multi-demo setup" or the "Product Demos | Single demo setup" and select 'Network' in the "Product Demos" deployment, or utilize the steps in the repo level README.

### Project

These demos leverage playbooks from a [git repo](https://github.com/nleiva/ansible-net-modules) that is added as the **`Network Golden Configs`** Project in your Ansible Controller. Review this repo for the playbooks to configure different resources and network config templates that will be configured.

### Inventory

These demos leverage "always-on" instances for Cisco IOS, IOSXR, and NXOS from [Cisco DevNet Sandboxes](https://developer.cisco.com/docs/sandbox/#!getting-started/always-on-sandboxes). These instances are shared and do not provide admin access but they are instantly avaible all the time meaning no setup time is required.

A **`Demo Inventory`** is created when setting up these demos and a dynamic source is added to populate the Always-On instances. Review the inventory file [here](https://github.com/nleiva/ansible-net-modules/blob/main/hosts).  Demo Inventory is the default inventory for **`Product Demos`**.

## Suggested Usage

**NETWORK / Report** - Use this job to gather facts from Cisco Network devices and create a report with information about the device such as code version, along with configuration information about layers 1, 2, and 3.  This shows how Ansible can be used to gather facts and build reports.  Generating html pages is just one potential output.  This information can be used in a number of ways, such as integration with different network management tools.
  - to run this you will first need to run the **`Deploy Cloud Stack in AWS`** job template to deploy the report server.  If using a demo.redhat.com Product Demos instance you should use the public key provided in the demo page in the Bastion Host Credentials section. If you are using a different environment, you may need to update the "Demo Credential".

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

**NETWORK / DISA STIG** - Use this job to run the DISA STIG role (in check mode) and show how Ansible can be used for configuration compliance of network devices.  Click into tasks to see what is changed for each compliance rule, i.e.:
{
  "changed": true,
  "warnings": [
    "To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if present in the running configuration on device"
  ],
  "commands": [
    "ip http max-connections 2"
  ],
  "updates": [
    "ip http max-connections 2"
  ],
  "banners": {},
  "invocation": {
    "module_args": {
      "defaults": true,
      "lines": [
        "ip http max-connections 2"
      ],
      "match": "line",
      "replace": "line",
      "multiline_delimiter": "@",
      "backup": false,
      "save_when": "never",
      "src": null,
      "parents": null,
      "before": null,
      "after": null,
      "running_config": null,
      "intended_config": null,
      "backup_options": null,
      "diff_against": null,
      "diff_ignore_lines": null
    }
  },
  "_ansible_no_log": false
}

**NETWORK / BACKUP** - Use this job to show how Ansible can be used to backup network devices using Red Hat validated content. Job Template will create a backup file on the reports server where they can be viewed as a webpage.  This is just an example - backups can also be sent to other repositories such as a Git repo (Github, Gitlab, etc).

To run this demo, you will need to complete a couple of prerequisites:
  - to run this you will first need to run the **`Deploy Cloud Stack in AWS`** job template to deploy the report server.
  - If using a demo.redhat.com Product Demos instance you should use the public key provided in the demo page in the 'Bastion Host Credentials' section. If you are using a different environment, you may need to update the "Demo Credential".
  - This works with Product Demos for AAP v2.5; which includes the "Product Demos EE" includes the \
  network.backup collection.
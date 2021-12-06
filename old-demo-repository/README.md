# Official Ansible Product Demos

This repo currently under construction and working on a minimal viable demo for testing purposes

## Table of contents

- [How to use](#how-to-use)
  - [1. Provide login information and choose demo](#1-provide-login-information-and-choose-demo)
  - [2. Run Ansible Playbook](#2-run-ansible-playbook)
- [Demo Repository](#demo-repository)
  - [Infrastructure Demos](#infrastructure-demos)
  - [Network Demos](#network-demos)
  - [Security Demos](#security-demos)
  - [Developer Demos](#developer-demos)
- [Contribute](#contribute)
- [Notes](#notes)

## How to use

## 1. Provide login information and choose demo

- Modify the `choose_demo.yml` file that is included in this repo with the username, password and IP address (or DNS name) of your Ansible Tower
- Choose the demo name you want from the table below (or choose `all`)

## 2. Run Ansible Playbook

```shell
ansible-playbook playbooks/install_demo.yml -e @choose_demo.yml
```

## Demo Repository

This repository currently holds 23 demos.

## Infrastructure Demos

| Demo Name | Author | install_demo.yml value | Description | Video Walkthrough | Workshop Types |
| --------- | ------ | ---------------------- | ----------- | ----------------- | -------------- |
| [INFRASTRUCTURE / AWS Provision VM](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/azure_provision_vm.md") | David Rojas | `demo: aws_provision_vm` | Provision RHEL VM on AWS with Ansible Tower Survey and Environmental variables | Not available  |  <li>windows</li> <li>demo</li> |
| [INFRASTRUCTURE / Azure create a MySQL Server](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/azure_mysql_server.md") | David Rojas | `demo: azure_mysql_server` | Provision MySQL server on Azure with Ansible Tower Survey and Environmental variables | Not available  |  <li>windows</li> <li>demo</li> |
| [INFRASTRUCTURE / Azure Provision VM](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/azure_provision_vm.md") | David Rojas | `demo: azure_provision_vm` | Provision RHEL VM on Azure with Ansible Tower Survey and Environmental variables | Not available  |  <li>windows</li> <li>demo</li> |
| [INFRASTRUCTURE / Chocolatey App Install](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/chocolatey_app_install.md") | David Rojas | `demo: chocolatey_app_install` | Install various application packages using Chocolatey from a survey | Not available  |  <li>windows</li> <li>demo</li> |
| [INFRASTRUCTURE / Chocolatey Config](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/chocolatey_config.md") | David Rojas | `demo: chocolatey_config` | Configure Chocolatey parameters that require not just enabling but adding values | Not available  |  <li>windows</li> <li>demo</li> |
| [INFRASTRUCTURE / Chocolatey Features Config](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/chocolatey_features.md") | David Rojas | `demo: chocolatey_features` | Enable or disable various Chocolatey features | Not available  |  <li>windows</li> <li>demo</li> |
| [INFRASTRUCTURE / Deploy Application](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/deploy_application.md") | Sean Cavanaugh | `demo: deploy_application` | install yum applications on Linux with a survey | [Video Link](https://www.youtube.com/watch?v=pU8ZgSBuEJw&list=PLdu06OJoEf2bp-PNtxPP_2n7Avkax8TED) |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |
| INFRASTRUCTURE / Fact Scan | Will Tome | `demo: fact_scan` | scan facts for Linux and Windows systems | Not available  |  <li>f5</li> <li>rhel</li> <li>windows</li> <li>rhel_90</li> <li>demo</li> |
| INFRASTRUCTURE / Gather Debug Info | Will Tome | `demo: debug_info` | provide info for memory and CPU usage for specified systems | Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |
| INFRASTRUCTURE / Grant Sudo | Will Tome | `demo: grant_sudo` | grant sudo privledges for specified time via survey | Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |
| INFRASTRUCTURE / Patching | Will Tome | `demo: patching` | patching for Linux servers | Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |
| INFRASTRUCTURE / Red Hat Insights | Sean Cavanaugh | `demo: insights` | install and configure Red Hat Insights | Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |
| INFRASTRUCTURE / Security Patching | Will Tome | `demo: security_patching` | upgrade all yum packages for security related except kernel | Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |
| INFRASTRUCTURE / Turn off IBM Community Grid | Sean Cavanaugh | `demo: turn_off_community_grid` | this role turns off IBM Community Grid boinc-client | Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |
| [INFRASTRUCTURE / Windows regedit legal notice](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/windows_regedit_legal_notice.md") | David Rojas | `demo: windows_regedit_legal_notice` | using regedit modify the legal notice | Not available  |  <li>windows</li> <li>demo</li> |
| SERVER / Windows IIS Server | Colin McNaughton | `demo: windows_iis` | install webserver on Windows Server with a survey | Not available  |  <li>windows</li> <li>demo</li> |

## Network Demos

| Demo Name | Author | install_demo.yml value | Description | Video Walkthrough | Workshop Types |
| --------- | ------ | ---------------------- | ----------- | ----------------- | -------------- |
| Cisco IOS logging config audit/remediation | Colin McCarthy | `demo: configlet_logging` | Cisco IOS logging config audit/remediation | Not available  |  <li>network</li> <li>demo</li> |
| Cisco IOS ntp config audit/remediation | Colin McCarthy | `demo: configlet_ntp` | Cisco IOS ntp config audit/remediation | Not available  |  <li>network</li> <li>demo</li> |
| Cisco IOS VTY ACL config audit/remediation | George James | `demo: configlet_vtyacl` | Cisco IOS VTY ACL config audit/remediation | Not available  |  <li>network</li> <li>demo</li> |
| NETWORK / WORKFLOW - F5 BIG-IP | Sean Cavanaugh | `demo: f5_bigip_workflow` | Workflow for F5 BIG-IP to setup a VIP (Virtual IP) load balancer between two RHEL webservers | Not available  |  <li>f5</li> <li>demo</li> |

## Security Demos

| Demo Name | Author | install_demo.yml value | Description | Video Walkthrough | Workshop Types |
| --------- | ------ | ---------------------- | ----------- | ----------------- | -------------- |
| SECURITY / Create Openscap Report | Sean Cavanaugh | `demo: openscap` | Create HTML report using SCAP Security Guide (SSG) | Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |
| SECURITY / Hardening | Will Tome | `demo: hardening` | hardening for Linux servers | Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |

## Developer Demos

| Demo Name | Author | install_demo.yml value | Description | Video Walkthrough | Workshop Types |
| --------- | ------ | ---------------------- | ----------- | ----------------- | -------------- |
| DEVELOPER / Create Developer Report | Sean Cavanaugh | `demo: developer_report` |Create HTML report using [Ansible facts](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variables-discovered-from-systems-facts)
| Not available  |  <li>f5</li> <li>rhel</li> <li>rhel_90</li> <li>demo</li> |

## Contribute

Please refer to the [contribute.md](docs/contribute.md) documentation included in this collection.

## Notes

This README.md was auto-generated by Ansible user **chadmf*- on **2021-12-06*- with Ansible version **2.9.27**

To generate a README.md, execute the following command

```shell
ansible-playbook playbooks/generate_readme.yml
```

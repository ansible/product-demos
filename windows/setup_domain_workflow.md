# Setup Active Directory Domain

A workflow to create a domain controller with two domain-joined Windows hosts.

## The Workflow

![Workflow Visualization](../.github/images/setup_domain_workflow.png)

## Ansible Inventory

There are additional groups created in the **Demo Inventory** for interacting with different components of the domain:

- **deployment_domain_ansible_local**: all hosts in the domain
- **purpose_domain_controller**: domain controller instances (1)
- **purpose_domain_computer**: domain computers (2)

_... graphic to come ..._

## Domain (ansible.local)

_... graphic to come ..._
# Setup Active Directory Domain

A workflow to create a domain controller with two domain-joined Windows hosts.

## The Workflow

![Workflow Visualization](../.github/images/setup_domain_workflow.png)

## Ansible Inventory

There are additional groups created in the **Demo Inventory** for interacting with different components of the domain:

- **deployment_domain_ansible_local**: all hosts in the domain
- **purpose_domain_controller**: domain controller instances (1)
- **purpose_domain_computer**: domain computers (2)

![Inventory](../.github/images/setup_domain_workflow_inventory.png)

## Domain (ansible.local)

![Domain Topology](../.github/images/setup_domain_workflow_domain.png)

## PowerShell Validation

In the validation step, you can expect to see the following output based on querying AD computers:

![Expected Output](../.github/images/setup_domain_final_state.png)

# Setup Active Directory Domain

A workflow to create a domain controller with two domain-joined Windows hosts.

## The Workflow

### High-Level

![Workflow Visualization Full](../.github/images/setup_domain_workflow_full.png)

### Close-Up

<img src="../.github/images/setup_domain_workflow_1.png" alt="Workflow Visualization Part 1" style="height: 250; width: auto"/>
<img src="../.github/images/setup_domain_workflow_2.png" alt="Workflow Visualization Part 2" style="height: 250; width: auto"/>
<img src="../.github/images/setup_domain_workflow_3.png" alt="Workflow Visualization Part 3" style="height: 250; width: auto"/>

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

# Ansible Windows Automated System Recovery (including 0-Day BSoD)

This Ansible project provides a comprehensive framework for automating Windows system recovery, with a particular focus on handling critical scenarios such as Blue Screen of Death (BSoD) incidents. Inspired by real-world challenges like the [2024 Crowdstrike incident](https://en.wikipedia.org/wiki/2024_CrowdStrike_incident), this framework demonstrates how to leverage Red Hat Ansible Automation Platform for rapid, scalable recovery across diverse Windows environments. While initially conceived for BSoD scenarios, the principles and techniques showcased here can be adapted for a wide range of Windows system recovery needs, offering a flexible, automated approach to maintaining system health and minimizing downtime in both VMware and OpenShift Virtualization platforms.

## Project Overview

The project consists of several playbooks and roles that allow you to:

1. Generate a Windows Preinstallation Environment (WinPE) ISO
2. Upload the WinPE ISO to your virtualization platform
3. Simulate a BSoD scenario
4. Boot a problematic VM into WinPE
5. Apply fixes to recover from the BSoD

### Ansible Automation Platform - Windows 0-Day BSoD Recovery (VMware vSphere)

https://github.com/user-attachments/assets/58c25289-00c6-4175-bd14-412b436eb5e4

### Ansible Automation Platform - Windows 0-Day BSoD Recovery (OpenShift Virtualization)

<a href="https://github.com/user-attachments/assets/dcd3c642-4da3-4646-8bc3-0320fbbc1868">
  <img src="https://img.shields.io/badge/Watch-Ansible%20Demo-red?style=for-the-badge&logo=ansible" alt="OpenShift Virtualization" title="Click to view Demo">
</a>

## Project Overview Podcast (AI-Generated)

Listen to an AI-generated discussion about this project:

https://github.com/user-attachments/assets/2427204c-bcc2-4c20-950b-fabd98c01da9

*Note: This podcast is AI-generated based on the project's README and other related content. It's intended as an experimental, supplementary way to learn about the project. Please treat it as a fun, unofficial overview rather than a definitive technical resource.*

We'd love to hear your thoughts on this AI-generated content! Join the discussion in our [GitHub Discussions](https://github.com/oatakan/ansible-windows-0-day-bsod-recovery/discussions) section.

- Did you find the podcast helpful or engaging?
- What aspects of the project would you like to hear discussed in more detail?
- How can we improve our project communication?

## Architecture and Workflow

The following diagram illustrates the high-level architecture and workflow of the BSoD recovery process:

![Architecture Diagram](media/architecture.svg)

## How to Use

1. Clone this repository to your local machine or Ansible control node.
2. Ensure you have Ansible installed (version 2.9 or higher recommended).
3. Install required collections: `ansible-galaxy collection install -r collections/requirements.yml`
4. Install required roles: `ansible-galaxy role install -r roles/requirements.yml`
5. Modify the `group_vars/all.yml` file to match your environment settings.
6. Choose the appropriate playbook for your scenario and run it using `ansible-playbook`.

## Scenarios and Playbooks

### Scenario 1: Generate and Upload WinPE

- `generate_winpe.yml`: Creates a custom WinPE ISO with recovery scripts. This is where the specific fix (e.g., for CrowdStrike-like issues or other BSoD scenarios) is embedded.
- `upload_winpe_iso.yml`: Uploads the generated WinPE ISO to the virtualization platform.

### Scenario 2: Simulate BSoD and Recovery

- `produce_bsod.yml`: Triggers a simulated BSoD on target Windows VMs.
- `execute_winpe_recovery.yml`: Boots the VM into WinPE and executes the embedded recovery script.
- `check_system.yml`: Performs a health check on the Windows systems after recovery.

## Project Background and Workflow

This project was inspired by the [2024 CrowdStrike incident](https://en.wikipedia.org/wiki/2024_CrowdStrike_incident), where a widespread BSoD issue affected numerous Windows systems. However, the project's scope extends beyond this single incident, providing a framework for automating recovery from various BSoD scenarios.

The workflow is designed as follows:

1. **WinPE Generation**: The `generate_winpe.yml` playbook creates a custom WinPE ISO. This ISO includes specific scripts tailored to address particular BSoD scenarios, such as the CrowdStrike-like issue or other common BSoD causes. The recovery logic is embedded within this ISO.

2. **Recovery Execution**: The `execute_winpe_recovery.yml` playbook is a generic orchestrator. It's responsible for:
   - Booting the affected VM into the custom WinPE environment
   - Initiating the embedded recovery script
   - Monitoring the recovery process
   - Handling the VM reboot after successful recovery

This design allows for great flexibility:

- To address different BSoD scenarios, you only need to modify the recovery script embedded in the WinPE ISO during the generation phase.
- The execution playbook remains consistent across various BSoD types, providing a unified interface for recovery operations.

By separating the specific recovery logic (in the WinPE ISO) from the execution process, this project offers a scalable and adaptable solution for automated Windows system recovery.

## Importing to Ansible Automation Platform (AAP)

To import this project into AAP:

1. Ensure you have access to an AAP instance.
2. Modify the `setup_demo.yml` playbook to match your AAP environment settings.
3. Run the `setup_demo.yml` playbook. This playbook will:
   - Create necessary inventories
   - Set up job templates
   - Configure projects
   - Set up workflows
4. Once imported, you can access and run the workflow templates from the AAP web interface.

## Project Structure

- `roles/`: Contains custom roles for WinPE creation, VM operations, and BSoD fixes.
- `group_vars/`: Stores common variables for the project.
- `node-config/`: Contains node-specific configurations for different scenarios.
- `collections/`: Lists required Ansible collections.
- `aap_config/`: Holds AAP-specific configuration files.

**Note:** This project is for demonstration purposes only and should not be used in production environments without proper testing and validation.

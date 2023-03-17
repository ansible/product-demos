# Linux Demos

## Table of Contents
- [Linux Demos](#linux-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
    - [Jobs](#jobs)
    - [Inventory](#inventory)
  - [Post Setup Job Steps](#post-setup-job-steps)
    - [Add Red Hat account details](#add-red-hat-account-details)
    - [Update Credentials for Insights Inventory](#update-credentials-for-insights-inventory)
    - [Add Variables for System Roles](#add-variables-for-system-roles)
  - [Suggested Usage](#suggested-usage)

## About These Demos
This category of demos shows examples of linux operations and management with Ansible Automation Platform. The list of demos can be found below. See the [Suggested Usage](#suggested-usage) section of this document for recommendations on how to best use these demos.

### Jobs
- [**Linux / Register**](ec2_register.yml) - Register a RHEL server with Red Hat Portal and Insights
- [**Linux / Troubleshoot**](tshoot.yml) - Run troubleshooting commands to find top CPU and memory users on the system
- [**Linux / Temporary Sudo**](temp_sudo.yml) - Grant temporary sudo access to a user on the system with time based cleanup
- [**Linux / Patching**](patching.yml) - Apply updates and/or generate patch report for linux systems
- [**Linux / Start Service**](service_start.yml) - Start a service on a system
- [**Linux / Stop Service**](service_stop.yml) - Stop a service on a system
- [**Linux / Run Shell Script**](run_script.yml) - Run a shell script or command on a system
- [**Linux / Fact Scan**](https://github.com/ansible/awx-facts-playbooks/blob/master/scan_facts.yml) - Run a fact, package, and service scan against a system and store in fact cache
- [**Linux / Podman Webserver**](podman.yml) - Install and run a Podman webserver with given text on the home page
- [**Linux / System Roles**](system_roles.yml) - Apply Linux system roles to servers. Must provide variables and role names.
- [**Linux / Compliance Enforce**](compliance.yml) - Apply remediation to meet the requirements of a compliance baseline
- [**Linux / Insights Compliance Scan**](insights_compliance_scan.yml) - Run a Compliance scan based on the configuration in [Red Hat Insights][https://console.redhat.com]

### Inventory

A dymanic inventory is created to pull inventory hosts from Red Hat Insights. The Systems will be added by their host name therefore adding duplicate systems will cause conflicts in the inventory. Only systems with the tag `purpose=demo` in Red Hat Insights will be added to this inventory. Groups will be created for other tags given to the system.

Groups will also be created for systems with missing security, enhancement and bug updates. The inventory configuration is governed by the [inventory.insights.yml](inventory.insights.yml) file.

> Remember to delete systems from your Red Hat account when you are done with the demo to avoid conflicts with future demos using the same names.

## Post Setup Job Steps
After running the setup job template, there are a few steps required to make the demos fully functional. See the post setup steps below.

> These steps may differ in your environment

### Add Red Hat account details
To register systems to the Red Hat portal and Insights, edit `extra_vars` on the `Linux / Register` job to include your org_id and an [activation key](https://access.redhat.com/management/activation_keys) to use when registering the systems.

### Update Credentials for Insights Inventory
Navigate to the Credentials section and update the `Insights Inventory` credential with your Red Hat Portal login.

### Add Variables for System Roles
Edit the `Linux / System Roles` job to include the list of roles that you wish to apply and the variables applicable for each role. See documentation [here](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles) for configuring System Roles.

## Suggested Usage
**Linux / Register** - Use this job to register systems to Red Hat Insights for showing Advisor recommendations and dynamic inventory.  Note that the "Ansible Group" will create an AAP inventory group, as well as tag hosts with that group name in Insights.

**Linux / Troubleshoot** - Use this job to show incident response troubleshooting and basic running of commands with an Ansible Playbook.

**Linux / Temporary Sudo** - Use this job to show how to grant sudo access with automated cleanup to a server. The user must exist on the system. Using the student user is a good example (ie. student1)

**Linux / Patching** - Use this job to apply updates or audit for missing updates and produce an html report of systems with missing updates. See the end of the job for the URL to view the report. In other environments this report could be uploaded to a wiki, email, other system. This demo also shows installing a webserver on a linux server. The report is places on the system defined by the `report_server` variable. By default, `report_server` is configured as `node1`. This may be overridden with `extra_vars` on the Job Template.

**Linux / Run Shell Script** - Use this job to demonstrate running shell commands or an existing shell script across a group of systems as root. This can be preferred over using Ad-Hoc commands due to the ability to control usage with RBAC. This is helpful in showing the scalable of execution of an existing shell script. It is always recommended to convert shell scripts to playbooks over time. Example usage would be getting the public key used in the environment with the command `cat .ssh/authorized_keys`.

**Linux / Fact Scan** - Use this job to demonstrate the use of the Ansible Fact Cache, Ansible facts, and the ability to query installed packages and running services on a system.

**Linux / Podman Webserver** - Use this job show managing individual containers with Podman via an Ansible Playbook.

**Linux / System Roles** - This job demonstrates running [RHEL System Roles with AAP. See the documentation [here](https://console.redhat.com/ansible/automation-hub/repo/published/redhat/rhel_system_roles) for how to configure system roles with variables by editing the extra_vars on the job template.

Example 1:
```
system_roles:
  - selinux

selinux_state: enforcing
```

Example 2 (less invasive, and runs faster):
```
system_roles:
  - timesync

timesync_ntp_servers:
  - hostname: pool.ntp.org
    pool: yes
    iburst: yes
```
**Linux / Compliance** - Apply compliance profile hardening configuration from [here](https://galaxy.ansible.com/RedHatOfficial). BE AWARE: this could have unintended results based on the current state of your machine. Always test on a single machine before distributing at scale. For example, AWS instances have NOPASSWD allowed for sudo. Running STIG compliance without adding `sudo_remove_nopasswd: false` to extra_vars on the job template will lock you out of the machine. This variable is configured on the job template by default for this reason.

**Linux / Insights Compliance Scan** - Scan the system according to the compliance profile configured via [Red Hat Insights](https://console.redhat.com). NOTE: This job will fail if the systems haven't been registered with Insights and associated with a relevant compliance profile. A survey when running the job will ask if you have configured all systems with a compliance profile, and effectively skip all tasks in the job template if the answer is "No".

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

### Workflows

| Workflow | Description |
|----------|-------------|
| [**Compliance Workflow**](docs/linux-compliance-workflow.md) | End-to-end compliance workflow that generates an OpenSCAP report, refreshes inventory, and enforces remediation on findings. |

### Jobs

| Job Template | Description |
|--------------|-------------|
| [**Register with Insights**](docs/linux-register-insights.md) | Register a RHEL server with the Red Hat Portal and Insights using an activation key and org ID. |
| [**Troubleshoot**](docs/linux-troubleshoot.md) | Run troubleshooting commands to find top CPU and memory consumers on a system for incident response. |
| [**Temporary Sudo**](docs/linux-temporary-sudo.md) | Grant temporary sudo access to a user with automatic time-based cleanup. |
| [**Patching**](docs/linux-patching.md) | Apply updates or audit for missing patches and produce an HTML report of systems with missing updates. |
| [**Start Service**](docs/linux-start-service.md) | Start a named service on a target system. |
| [**Stop Service**](docs/linux-stop-service.md) | Stop a named service on a target system. |
| [**Run Shell Script**](docs/linux-run-shell-script.md) | Execute a shell script or command across a group of systems as root, with RBAC-controlled access. |
| [**Fact Scan**](docs/linux-fact-scan.md) | Run a fact, package, and service scan against a system and store results in the AAP fact cache. |
| [**Podman Webserver**](docs/linux-podman-webserver.md) | Install and run an Apache webserver in a Podman container with a configurable home page message. |
| [**System Roles**](docs/linux-system-roles.md) | Apply RHEL System Roles (e.g. SELinux, timesync) to servers using the redhat.rhel_system_roles collection. |
| [**Install Web Console (Cockpit)**](docs/linux-cockpit.md) | Install and configure the RHEL Web Console (Cockpit) using the cockpit system role with minimal, default, or full package sets. |
| [**Compliance Enforce**](docs/linux-compliance-enforce.md) | Remediate systems that are out of compliance by applying enforcement rules from a compliance scan. |
| [**DISA STIG**](docs/linux-disa-stig.md) | Apply the RHEL STIG security hardening configuration using DISA Supplemental Automation Content. |
| [**Multi-profile Compliance**](docs/linux-multi-profile-compliance.md) | Apply remediation from Compliance as Code to enforce CIS, HIPAA, OSPP, PCI-DSS, or STIG compliance profiles. |
| [**Multi-profile Compliance Report**](docs/linux-compliance-report.md) | Run an OpenSCAP report against a compliance profile and optionally serve results via httpd on the target host. |
| [**Insights Compliance Scan**](docs/linux-insights-compliance-scan.md) | Run a compliance scan based on profiles configured in Red Hat Insights. Systems must be registered and associated with a profile. |
| [**Deploy Application**](docs/linux-deploy-application.md) | Install a named application package on target systems. |

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

**Linux / Patching** - Use this job to apply updates or audit for missing updates and produce an html report of systems with missing updates. For a more comprehensive patching workflow that includes EC2 snapshots, pre/post verification, automatic rollback, and a compliance report across both RHEL and Windows, see [Patch Cloud Stack in AWS](../cloud/docs/patch-cloud-stack.md) in the Cloud demos. See the end of the job for the URL to view the report. In other environments this report could be uploaded to a wiki, email, other system. This demo also shows installing a webserver on a linux server. The report is places on the system defined by the `report_server` variable. By default, `report_server` is configured as `reports`. This may be overridden with `extra_vars` on the Job Template.

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
**Linux / DISA STIG** - Apply the RHEL STIG security hardening configuration using the [DISA Supplemental Automation Content](https://public.cyber.mil/stigs/supplemental-automation-content/). BE AWARE: this could have unintended results based on the current state of your machine. Always test on a single machine before distributing at scale. For example, AWS instances have NOPASSWD allowed for sudo. Running STIG compliance without adding `sudo_remove_nopasswd: false` to extra_vars on the job template will lock you out of the machine. This variable is configured on the job template by default for this reason.

**Linux / Multi-profile Compliance** - Apply security hardening configuration from a [supported compliance profile role](compliance_profiles.md). BE AWARE: this could have unintended results based on the current state of your machine. Always test on a single machine before distributing at scale. For example, AWS instances have NOPASSWD allowed for sudo. Applying certain compliance profiles without adding `sudo_remove_nopasswd: false` to extra_vars on the job template will lock you out of the machine. This variable is configured on the job template by default for this reason.

**Linux / Report Compliance** - Run this template before running the "**Linux / Multi-profile Compliance**" template and again afterwards to highlight the changes made by the enforcement template.  By default, the reports are available by pointing a web browser to the system(s) where the report runs.  By setting the `use_httpd` variable to "false" in the template survey the reports will instead be stored on the target node in the /tmp/oscap-reports directory.

**Linux / Insights Compliance Scan** - Scan the system according to the compliance profile configured via [Red Hat Insights](https://console.redhat.com). NOTE: This job will fail if the systems haven't been registered with Insights and associated with a relevant compliance profile. A survey when running the job will ask if you have configured all systems with a compliance profile, and effectively skip all tasks in the job template if the answer is "No".

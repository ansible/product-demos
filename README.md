[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Dev Spaces](https://img.shields.io/badge/Customize%20Here-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://workspaces.openshift.com/f?url=https://github.com/ansible/product-demos)

# APD - Ansible Product Demos

The Ansible Product Demos (APD) project is a set of Ansible demos that run on the [Red Hat Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible) (AAP).  These demos are deployed using configuraton-as-code and playbooks that create AAP resources (such as projects, templates, and credentials) meant for demonstrating automation use cases in several technology domains:

| Demo Name | Description |
|-----------|-------------|
| [Linux](linux/README.md) | Repository of demos for RHEL and Linux automation |
| [Windows](windows/README.md) | Repository of demos for Windows Server automation |
| [Cloud](cloud/README.md) | Demo for infrastructure and cloud provisioning automation |
| [Network](network/README.md) | Network automation demos |
| [OpenShift](openshift/README.md) | OpenShift automation demos |
| [Satellite](satellite/README.md) | Demos of automation with Red Hat Satellite Server |

## Installation

APD can be added to an existing AAP deployment by running the installation playbook.  It relies on the [APD execution environment image](https://quay.io/repository/ansible-product-demos/apd-ee-25) for access to the modules and roles used to apply configuration-as-code to AAP.

### Installing with the installation playbook

1. Clone this repository
2. Set the following environment variables for authentication to your AAP deployment:

```
export AAP_HOSTNAME=https://your-aap-server.example.com

# either set AAP_USERNAME and AAP_PASSWORD for password auth to AAP
export AAP_USERNAME=admin  # or another AAP account with superuser privileges
export AAP_PASSWORD=<admin_user_password>

# or alternately set AAP_TOKEN if you have an admin token
#export AAP_TOKEN=<admin_user_token>
```
3. Use `ansible-navigator` to run the installation playbook using the APD execution environment image.  The ansible-navigator program must be installed as a prerequisite, either from the AAP package repository or from the [upstream ansible-dev-tools PyPI package](https://pypi.org/project/ansible-dev-tools/).

```
ansible-navigator run -m stdout install-apd.yml
```

### Use a pre-installed APD environment on the Red Hat Demo Platform (account required)

For Red Hat associates and partners, there is an Ansible Product Demos catalog item [available on demo.redhat.com](https://red.ht/apd-sandbox) that provides a pre-installed environment for demo purposes.  An existing account is required for access to the Red Hat Demo Platform system.

## Bring Your Own Demo

Can't find what you're looking for? Customize this repo to make it your own.

1. Create a fork of this repo.
2. Update the URL of the `Ansible Project Demos` project your Ansible Automation Platform controller.
3. Make changes to your fork as needed and run the **Product Demos | Single demo setup** job

See the [contributing guide](CONTRIBUTING.md) for more details on how to customize the project.

---

[Privacy statement](https://www.redhat.com/en/about/privacy-policy) | [Terms of use](https://www.redhat.com/en/about/terms-use) | [Security disclosure](https://www.ansible.com/security?hsLang=en-us) | [All policies and guidelines](https://www.redhat.com/en/about/all-policies-guidelines)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Dev Spaces](https://img.shields.io/badge/Customize%20Here-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://workspaces.openshift.com/f?url=https://github.com/ansible/product-demos)

# APD - Ansible Product Demos

The Ansible Product Demos (APD) project is a set of Ansible demos that are deployed using [Red Hat Ansible Automation Platform](https://www.redhat.com/en/technologies/management/ansible).  It uses configuraton-as-code to create AAP resources such as projects, templates, and credentials that form the basis for demonstrating automation use cases in several technology domains:

| Demo Name | Description |
|-----------|-------------|
| [Linux](linux/README.md) | Repository of demos for RHEL and Linux automation |
| [Windows](windows/README.md) | Repository of demos for Windows Server automation |
| [Cloud](cloud/README.md) | Demo for infrastructure and cloud provisioning automation |
| [Network](network/README.md) | Network automation demos |
| [OpenShift](openshift/README.md) | OpenShift automation demos |
| [Satellite](satellite/README.md) | Demos of automation with Red Hat Satellite Server |

## Using this project

Use the [APD bootstrap](https://github.com/ansible/product-demos-bootstrap) repo to add APD to an existing Ansible Automation Platform deployment.  The bootstrap repo provides the initial manual prerequisite steps as well as a playbook for adding APD to the existing deployment.

For Red Hat associates and partners, there is an Ansible Product Demos catalog item [available on demo.redhat.com](https://red.ht/apd-sandbox) (account required).

## Bring Your Own Demo

Can't find what you're looking for? Customize this repo to make it your own.

1. Create a fork of this repo.
2. Update the URL of the `Ansible Project Demos` project your Ansible Automation Platform controller.
3. Make changes to your fork as needed and run the **Product Demos | Single demo setup** job

See the [contributing guide](CONTRIBUTING.md) for more details on how to customize the project.

---

[Privacy statement](https://www.redhat.com/en/about/privacy-policy) | [Terms of use](https://www.redhat.com/en/about/terms-use) | [Security disclosure](https://www.ansible.com/security?hsLang=en-us) | [All policies and guidelines](https://www.redhat.com/en/about/all-policies-guidelines)

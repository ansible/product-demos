# Contribute

So you want to create a demo?  What do you do? These demos are considered "demos as code" so every demo must adhere to our standards and be highly re-usable.

## Requirements

- Must work with Ansible Tower / Ansible Automation Platform.  There has to be a UX component to the demo.
- Must be ephemeral and require no service that cannot be reproduced in an automated fashion.  This means a demo that requires the user to create a personalized token with an external service (e.g. ServiceNow, Slack) is not appropriate here because it would require manual steps for a user to recreate your demo.
- Must align with Red Hat use-cases.  A demo that programs your lawn mower is not something we would actually demonstrate.  You can easily create a fork of this repo and make your own fun project.

You need **three** major components to get a demo accepted

## 1. Demo var file

In the principle of "everything as code", these are "demos as code".  Each demo has its own individual var file.  All var files are installed under:

  ```shell
  /roles/install_demo/vars/main
  ```

There are four categories of demos:

  1. **infrastructure** - automation for IT infrastructure such as Linux and Windows.
  2. **network** - automation for network infrastructure such as routers and switches.
  3. **security** - automation for SIEMs, firewalls, and IPS such as IBM Qradar, Splunk and Checkpoint.
  4. **developer** - automation for developer persona, such as CI/CD pipelines, web hooks, developer environments and automated testing

Look at a very specific example here: `deploy_application.yml`

Location: `roles/install_demo/vars/main/infrastructure/deploy_application.yml`
Link: [https://github.com/ansible/product-demos/blob/master/roles/install_demo/vars/main/infrastructure/deploy_application.yml](https://github.com/ansible/product-demos/blob/master/roles/install_demo/vars/main/infrastructure/deploy_application.yml)

## 2. Ansible Playbook

In the demo var file above you will notice a `playbook` line. For example in the `deploy_application.yml` example:

`playbook: "playbooks/infrastructure/deploy_application.yml"`

There is also a **project** section of the demo var file

```yml
project:
  name: "Ansible official demo project"
  description: "prescriptive demos from Red Hat Management Business Unit"
  organization: "Default"
  scm_type: git
  scm_url: "https://github.com/ansible/product-demos"
```

The Ansible Playbook **does NOT** have to exist in this repo.  In fact it is encouraged to fork this repo and test it out by pointing to your own repo.  It is also recommended to create Ansible Playbooks that work on the [Ansible Automation Workshop](https://github.com/ansible/workshops) topologies.  This makes them extremely re-usable.

## 3. Walkthrough

Each demo should have a walkthrough.  In the demo var file there is a line with the key `readme`.  For example for the `deploy_application.yml`:

```yml
readme: "https://github.com/ansible/product-demos/blob/master/docs/infrastructure/deploy_application.md"
```

Here is an example walkthrough for the `deploy_application.yml` demo: [https://github.com/ansible/product-demos/blob/master/docs/infrastructure/deploy_application.md](https://github.com/ansible/product-demos/blob/master/docs/infrastructure/deploy_application.md)

## Converting Existing Workflows into ephemeral demos

There is no way in the Ansible Tower API to access the workflow schema at this time (March 2020).  Please refer to the docs and use the awx-cli/tower-cli command to export existing Workflow schema: [https://github.com/ansible/tower-cli/blob/master/docs/source/cli_ref/usage/WORKFLOWS.rst](documentation).

The Workflow schema can be automated by using the [tower_workflow_template](https://docs.ansible.com/ansible/latest/modules/tower_workflow_template_module.html#parameter-schema) module to load Ansible Tower with an entire Workflow.

## update May 2020

The [awx.awx collection](https://galaxy.ansible.com/awx/awx) has some new enhancements to allow installation of Ansible workflows   Please coordinate with Ansible API team if you need help.

## Going Further

The following links will be helpful if you want to contribute code to the Ansible Workshops project, or any Ansible project:

- [Ansible Committer Guidelines](http://docs.ansible.com/ansible/latest/committer_guidelines.html)
- [Learning Git](https://git-scm.com/book/en/v2)

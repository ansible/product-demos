# Contribute

This project is **not** currently taking PRs (pull requests) or code contributions.  This is currently a work in progress and not at a point that would make sense to take contributions.  Please try to make PRs into [ansible-examples](https://github.com/ansible/ansible-examples) if you want to showcase Ansible Playbooks or roles.

# Converting Existing Workflows into ephemeral demos

There is no way in the Ansible Tower API to access the workflow schema at this time (March 2020).  Please refer to the docs and use the awx-cli/tower-cli command to export existing Workflow schema: [https://github.com/ansible/tower-cli/blob/master/docs/source/cli_ref/usage/WORKFLOWS.rst](documentation).

The Workflow schema can be automated by using the [tower_workflow_template](https://docs.ansible.com/ansible/latest/modules/tower_workflow_template_module.html#parameter-schema) module to load Ansible Tower with an entire Workflow.

# Going Further

The following links will be helpful if you want to contribute code to the Ansible Workshops project, or any Ansible project:
- [Ansible Committer Guidelines](http://docs.ansible.com/ansible/latest/committer_guidelines.html)
- [Learning Git](https://git-scm.com/book/en/v2)

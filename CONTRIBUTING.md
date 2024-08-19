# Contribution Guidelines
This document aims to outline the requirements for the various forms of contribution for this project.

## Project Architecture

![project-architecture](.github/images/project-architecture.png)

## Pull Requests

**ALL** contributions are subject to review via pull request

### Pull Requests
1) Ensure the "base repository" is set to "ansible/product-demos".

#### Pull Request Guidelines
- PRs should include the playbook/demo and required entry in corresponding `<demo>/setup.yml`.
- PRs should include documentation in corresponding `<demo>/README.md`.
- PRs should be rebased against the `main` branch to avoid conflicts.
- PRs should not impact more than a single directory/demo section.
- PRs should not rely on external infrastructure or configuration unless the dependency is automated or specified in the `user_message` of `setup.yml`.
- PR titles should describe the work done in the PR.  Titles should not be generic ("Added new demo") and should not refer to an issue number ("Fix for issue #123").

## Adding a New Demo
1) Create a new branch based on main. (eg. `git checkout -b <branch name>`)
2) Add your playbook to the appropriate demo/section subdirectory.
3) Make any changes needed to match the existing standards in the directory.
   1) Ex: Parameterized hosts
   ```ansible
   hosts: "{{ _hosts | default('windows') }}"
   ```
4) Create an entry for your playbook in your subdirectories `setup.yml`
   1) You can copy paste an existing one and edit it.
   2) Ensure you edit the name, playbook path, survey etc.
5) Add any needed roles/collections to the [requirements.yml](/collections/requirements.yml)
6) Test via [demo.redhat.com](https://demo.redhat.com/catalog?search=product&item=babylon-catalog-prod%2Fopenshift-cnv.aap-product-demos-cnv.prod), specifying your branch name within the project configuration.

> NOTE: demo.redhat.com is available to Red Hat Associates and Partners with a valid account.

## New Demo Section/Category
1) Create a new subdirectory with no spaces
2) Create a new setup.yml copying appropriate elements from another
   - Below is a sample skeleton for a new setup.yml
    ```ansible
    ---
    user_message: ''

    controller_templates:
    ...
    ```
   - Configuration variables can be from any of the roles defined in the [infra.controller_configuration collection](https://github.com/redhat-cop/controller_configuration/tree/devel/roles)
   - Add variables for each component listed
3) Include a README.md in the subdirectory

## Testing

We utilize pre-commit to handle Git hooks, initiating a pre-commit check with each commit, both locally and on CI.

To install pre-commit, use the following commands:
```bash
pip install pre-commit
pre-commit install
```

For further details, refer to the [pre-commit installation documentation](https://pre-commit.com/#installation).

To execute ansible-lint (whether within pre-commit or independently), you must configure an environment variable for the token required to connect to Automation Hub. Obtain the token [here](https://console.redhat.com/ansible/automation-hub/token).

Copy the token value and execute the following command:

```bash
export ANSIBLE_GALAXY_SERVER_AH_TOKEN=<token>
```

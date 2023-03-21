# Contribution Guidelines
This document aims to outline the requirements for the various forms of contribution for this project.

**ALL** contributions are subject to review via pull request

## Pull Requests
1) Ensure the "base repository" is set to "ansible/product-demos".

### Pull Request Guidelines
- PRs should include the playbook/demo and required entry in corresponding `<demo>/setup.yml`.
- PRs should include documentation in corresponding `<demo>/README.md`.
- PRs should be rebased against the `main` branch to avoid conflicts.
- PRs should not impact more than a single directory/demo section.
- PRs should not rely on external infrastructure or configuration unless the dependency is automated or specified in the `user_message` of `setup.yml`.

## Adding a New Demo
1) Create a new branch based on main. (eg. `git checkout -b <branch name>`)
2) Add your playbook to the appropriate demo/section subdirectory.
3) Make any changes needed to match the existing standards in the directory.
   1) Ex: Parameterized hosts
   ```ansible
   hosts: "{{ HOSTS | default('windows') }}"
   ```
4) Create an entry for your playbook in your subdirectories `setup.yml`
   1) You can copy paste an existing one and edit it.
   2) Ensure you edit the name, playbook path, survey etc.
5) Add any needed roles/collections to the [requirements.yml](/collections/requirements.yml)
6) Test via RHPDS, specify your branch name within the project configuration.

## New Demo Section/Category
1) Create a new subdirectory with no spaces
2) Create a new setup.yml copying appropriate elements from another
   - Below is a sample skeleton for a new setup.yml
    ```ansible
    ---
    user_message: ''

    controller_components:
    - job_templates

    controller_templates:
    ...
    ```
   - `controller_components` can be any of the roles defined [here](https://github.com/redhat-cop/controller_configuration/tree/devel/roles)
   - Add variables for each component listed
3) Include a README.md in the subdirectory

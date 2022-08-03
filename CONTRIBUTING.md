# Contribution Guidelines
This document aims to outline the requirements for the various forms of contribution for this project.

**ALL** contributions are subject to review via pull request

## Pull requests
1) Ensure the "base repository" is set to "RedHatGov/product-demos" since this is a fork it defaults to it's parent "ansible/product-demos".

## New playbooks
1) Create a new branch based on main
2) Add your playbook to the appropriate OS/System subdirectory
3) Make any changes needed to match the existing standards in the direcotory.
   1) Ex: Parameterized hosts
   ```ansible
   hosts: "{{ HOSTS | default('windows') }}"
   ```
4) Create an entry for your playbook in your subdirectories setup.yml
   1) You can copy paste an existing one and edit it.
   2) Ensure you edit the name, playbook path, survey etc.
5) Add any needed roles/collections to the [requirements.yml](/collections/requirements.yml)
6) Test via RHPDS, specify your branch name within the project configuration.

## New OS/Systems
1) Create a new subdirectory with no spaces
2) Create a new setup.yml copying appropriate elements from another
   1) These should all be mostly the same at the top
    ```ansible
    ---
    controller_components:
    - job_templates

    controller_templates:
    ...
    ```

# install_demo role

This role will install demos into your specified Ansible Tower environment.  Here is an example of using this role:

```
---
- name: setup deploy application demo
  hosts: localhost
  gather_facts: false
  connection: local

  tasks:

    - name: install demo
      include_role:
        name: "install_demo"
```

Please refer to the master list in the main [README.md]()../../README.md).

# required variables

You must specify all the variables in the [choose_demo.yml](../../choose_demo.yml) example.

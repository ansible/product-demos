vpc
=========
```
This role will create or delete a Amazon Virtual Private Cloud (VPC).
```
Requirements
------------
```
Amazon Web Console Account
Amazon Web Services Credential in Ansible Automation Platform
```
Role Variables
--------------
```
vpc_name: linux-dailydemo
vpc_cidr: 172.16.20.0/24
vpc_region: us-west-1
vpc_user_name: eric.ames
vpc_alwaysup: false
vpc_deleteby: hercules
vpc_ec2_ansible_group: "{{ vpc_user_name }}"
vpc_ec2_security_group_name: "{{ vpc_name }}_SECGRP"
vpc_ec2_vpc_subnet_name: "{{ vpc_name }}_Subnet"
vpc_ec2_rt_name: "{{ vpc_name }}_RT_Internet"
vpc_ec2_igw_name: "{{ vpc_name }}_IGW"
vpc_my_email_address: "{{ vpc_user_name }}@redhat.com"
ansible_python_interpreter: /usr/bin/python3
```
Dependencies
------------
```
amazon.aws
```
Example Playbook
----------------
```
---
- name: Create our vpc
  hosts: localhost
  connection: local

  tasks:

    - name: Include the vpc role
      tags:
        - create
      ansible.builtin.include_role:
        name: vpc

or

---
- name: Remove our vpc
  hosts: localhost
  connection: local

  tasks:

    - name: Include the vpc role
      tags:
        - remove
      ansible.builtin.include_role:
        name: vpc

```
License
-------

https://opensource.org/license/mit

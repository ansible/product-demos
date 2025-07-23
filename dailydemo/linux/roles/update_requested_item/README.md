update_requested_item
=========
```
Update requested item ticket in ServiceNow
```
Requirements
------------

Role Variables
--------------
```
update_requested_item_comments: |-
  Uh-Oh something broke.

  ServiceNow incident number: {{ create_incident_ticket }}

  Ansible Job ID: {{ vm_my_job_id }}

  Message: {{ vm_my_error }}
update_requested_item_state: 4
#
# Variable set at the workflow template
# ticket_number: ''
#
# Credential Types needed for this role
# ServiceNow ITSM Credential - This is a Custom Credential
```
Dependencies
------------

Example Playbook
----------------
```
---
- name: Update requested item ticket in servicenow
  hosts: localhost

  roles:

    - role: update_requested_item
```
License
-------

https://opensource.org/license/mit

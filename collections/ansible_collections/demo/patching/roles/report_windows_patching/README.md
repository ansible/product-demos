build_report_windows_patch
========

Installs Apache and creates a report based on facts from Windows update job

Requirements
------------

Must run on Apache server

Role Variables / Configuration
--------------

N/A

Dependencies
------------

N/A

Example Playbook
----------------

The role can be used to create an html patching report on any number of Linux hosts using any number of Windows servers


```
---
- hosts: all

  tasks:
  - name: Run Windows Patch Report
    import_role:
      name: shadowman.reports.build_report_windows_patch
      
```
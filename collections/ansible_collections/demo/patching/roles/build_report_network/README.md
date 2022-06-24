build_report_network
========

Installs Apache and creates a report based on facts from network devices

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

The role can be used to create an html report on any number of Linux hosts using any number of network devices


```
---
- hosts: all

  tasks:
  - name: Run Network Report
    import_role:
      name: shadowman.reports.build_report_network
      
```
build_report_linux
========

Installs Apache and creates a report based on facts from Linux services and packages modules

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

The role can be used to create an html report on any number of Linux hosts using any number of Linux servers about their services and packages installed


```
---
- hosts: all

  tasks:
  - name: Run Linux Report
    import_role:
      name: shadowman.reports.build_report_linux
      
```
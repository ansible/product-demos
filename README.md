# Official Ansible Product Demos

This repo currently under construction and working on a minimal viable demo for testing purposes

# Table of contents

   * [How to use](#how-to-use)
      * [1. Provide login information and choose demo](#1-provide-login-information-and-choose-demo)
      * [2. Run Ansible Playbook](#2-run-ansible-playbook)
   * [Demo Repository](#demo-repository)
      * [Infrastructure Demos](#infrastructure-demos)
      * [Network Demos](#network-demos)
      * [Security Demos](#security-demos)
      * [Developer Demos](#developer-demos)
   * [Contribute](#contribute)
   * [Notes](#notes)

# How to use

## 1. Provide login information and choose demo

  - Modify the `choose_demo.yml` file that is included in this repo with the username, password and IP address (or DNS name) of your Ansible Tower
  - Choose the demo name you want from the table below (or choose `all`)

## 2. Run Ansible Playbook

```
ansible-playbook playbooks/install_demo.yml -e @choose_demo.yml
```

# Demo Repository

This repository currently holds 11 demos.

## Infrastructure Demos
<table>
  <tr>
    <th>Demo Name</th>
    <th>Author</th>
    <th>install_demo.yml value</th>
    <th>Description</th>
    <th>Video Walkthrough</th>
    <th>Workshop Types</th>
  </tr>
  <tr>
    <td>Deploy Application (survey)</td>
    <td>Sean Cavanaugh</td>
    <td><pre>demo: deploy_application</pre></td>
    <td>install yum applications on Linux with a survey</td>
    <td><a href="https://www.youtube.com/watch?v=pU8ZgSBuEJw&list=PLdu06OJoEf2bp-PNtxPP_2n7Avkax8TED">Video Link</a></td>
    <td><ul><li>f5</li><li>rhel</li></ul></td>
  </tr>
  <tr>
    <td>SERVER / Fact Scan</td>
    <td>Will Tome</td>
    <td><pre>demo: fact_scan</pre></td>
    <td>scan facts for Linux and Windows systems</td>
    <td>Not available </td>
    <td><ul><li>f5</li><li>rhel</li><li>windows</li></ul></td>
  </tr>
  <tr>
    <td>SERVER / Gather Debug Info</td>
    <td>Will Tome</td>
    <td><pre>demo: debug_info</pre></td>
    <td>provide info for memory and CPU usage for specified systems</td>
    <td>Not available </td>
    <td><ul><li>f5</li><li>rhel</li></ul></td>
  </tr>
  <tr>
    <td>SERVER / Grant Sudo</td>
    <td>Will Tome</td>
    <td><pre>demo: grant_sudo</pre></td>
    <td>grant sudo privledges for specified time via survey</td>
    <td>Not available </td>
    <td><ul><li>f5</li><li>rhel</li></ul></td>
  </tr>
  <tr>
    <td>SERVER / Patching</td>
    <td>Will Tome</td>
    <td><pre>demo: patching</pre></td>
    <td>patching for Linux servers</td>
    <td>Not available </td>
    <td><ul><li>f5</li><li>rhel</li></ul></td>
  </tr>
  <tr>
    <td>SERVER / Security Patching</td>
    <td>Will Tome</td>
    <td><pre>demo: security_patching</pre></td>
    <td>upgrade all yum packages for security related except kernel</td>
    <td>Not available </td>
    <td><ul><li>f5</li><li>rhel</li></ul></td>
  </tr>
  <tr>
    <td>Windows IIS Server</td>
    <td>Colin McNaughton</td>
    <td><pre>demo: windows_iis</pre></td>
    <td>install webserver on Windows Server with a survey</td>
    <td>Not available </td>
    <td><ul><li>windows</li></ul></td>
  </tr>
</table>

## Network Demos

<table>
  <tr>
    <th>Demo Name</th>
    <th>Author</th>
    <th>install_demo.yml value</th>
    <th>Description</th>
    <th>Video Walkthrough</th>
    <th>Workshop Types</th>
  </tr>
  <tr>
    <td>WORKFLOW - F5 BIG-IP</td>
    <td>Sean Cavanaugh</td>
    <td><pre>demo: f5_bigip_workflow</pre></td>
    <td>Workflow for F5 BIG-IP to setup a VIP (Virtual IP) load balancer between two RHEL webservers</td>
    <td>Not available </td>
    <td><ul><li>f5</li></ul></td>
  </tr>
</table>

## Security Demos

<table>
  <tr>
    <th>Demo Name</th>
    <th>Author</th>
    <th>install_demo.yml value</th>
    <th>Description</th>
    <th>Video Walkthrough</th>
    <th>Workshop Types</th>
  </tr>
  <tr>
    <td>Create Openscap Report</td>
    <td>Sean Cavanaugh</td>
    <td><pre>demo: openscap</pre></td>
    <td>Create HTML report using SCAP Security Guide (SSG)</td>
    <td>Not available </td>
    <td><ul><li>f5</li><li>rhel</li></ul></td>
  </tr>
  <tr>
    <td>SERVER / Hardening</td>
    <td>Will Tome</td>
    <td><pre>demo: hardening</pre></td>
    <td>hardening for Linux servers</td>
    <td>Not available </td>
    <td><ul><li>f5</li><li>rhel</li></ul></td>
  </tr>
</table>

## Developer Demos

<table>
  <tr>
    <th>Demo Name</th>
    <th>Author</th>
    <th>install_demo.yml value</th>
    <th>Description</th>
    <th>Video Walkthrough</th>
    <th>Workshop Types</th>
  </tr>
  <tr>
    <td>Create Developer Report</td>
    <td>Sean Cavanaugh</td>
    <td><pre>demo: developer_report</pre></td>
    <td>Create HTML report using <a href="https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#variables-discovered-from-systems-facts">Ansible facts</a></td>
    <td>Not available </td>
    <td><ul><li>f5</li><li>rhel</li></ul></td>
  </tr>
</table>


# Contribute

please refer to the [contribute.md](docs/contribute.md) documentation included in this collection.

# Notes

This README.md was auto-generated by Ansible user **sean** on **2020-03-12** with Ansible version **2.9.5**

To generate a README.md, execute the following command

```
ansible-playbook playbooks/generate_readme.yml
```

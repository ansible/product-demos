# Official Ansible Product Demos

this is currently under construction and working on a minimal viable demo for testing purposes

# How to use

## 1. Provide login information and choose demo

  - Modify the `choose_demo.yml` file that is included in this repo with the username, password and IP address (or DNS name) of your Ansible Tower
  - Choose the demo name you want from the table below (or choose `all`)

## 2. Run Ansible Playbook

```
ansible-playbook playbooks/install_demo.yml -e @choose_demo.yml
```

# Demo Repository

<table>
  <tr>
    <th>Demo Name</th>
    <th>Description</th>
    <th>Video Walkthrough</th>
    <th>Workshop Types</th>
  </tr>
  <tr>
    <td>Deploy Application</td>
    <td>simple survey to install yum applications on Linux</td>
    <td><a href="https://www.youtube.com/watch?v=pU8ZgSBuEJw&list=PLdu06OJoEf2bp-PNtxPP_2n7Avkax8TED&index=1">Youtube Video</a></td>
    <td>
    <ul>
    <li>f5</li>
    <li>rhel</li>
    </ul>
    </td>
  </tr>
  <tr>
    <td>Openscap</td>
    <td>Create HTML report using SCAP Security Guide (SSG)</td>
    <td>Not Available</td>
    <td>
    <ul>
    <li>f5</li>
    <li>rhel</li>
    </ul>
    </td>
  </tr>
</table>

# Contribute

please refer to the [contribute.md](docs/contribute.md) documentation included in this collection.

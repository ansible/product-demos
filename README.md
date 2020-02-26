# Official Ansible Product Demos

this is currently under construction and working on a minimal viable demo for testing purposes

# How to use

## 1. Provide login information for Ansible Tower

Modify the `tower_login_info.yml` that is included in this repo with the username, password and IP address (or DNS name) of your Ansible Tower

## 2. Choose your demo

Modify the `choose_demo.yml` that is included in this repo with demo name you want.

## 3. Run Ansible Playbook

```
ansible-playbook playbooks/install_demo.yml -e @choose_demo.yml -e @tower_login_info.yml
```

# Demo Repository

<table">
  <tr>
    <th>Demo Name</th>
    <th>Description</th>
    <th>Workshop Types</th>
  </tr>
  <tr>
    <td>Deploy Application</td>
    <td>simple survey to install yum applications on Linux</td>
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

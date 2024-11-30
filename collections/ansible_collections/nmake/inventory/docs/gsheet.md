# Ansible inventory using a google sheet

## Requirements

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Set-up

1) Clone the repository

2) Link the repo into the default collection path

    ```
    mkdir -p ~/.ansible/collections/ansible_collections/nmake
    ln -s ~/projects/inventory ~/.ansible/collections/ansible_collections/nmake
    ```

3) Enable the Google sheets API and download the `credentials.json` file.

    https://developers.google.com/sheets/api/quickstart/python

4) Create the token file by running the inventory script directly from the command line

    Note:
    - Provide the full path the credentials file downloaded above
    - Provide a path to where the token file should be created
    - This step is optional, if not completed the token file will be created during the first use of the inventory plugin


    ```shell
    python /path_to_repo/inventory/plugins/inventory/gsheet.py \
      --token /home/username/token.pickle \
      --credentials /home/username/credentials.json
    ```

5) Build the google sheet

    Note-

    - Take note of the spreadsheet ID in the URL for your google sheet
    - The inventory will be build from the first sheet only

    Sample URL and sheet ID
    ```
    https://docs.google.com/spreadsheets/d/1iTRfuFTPidnJoplKVH4e5znlk3my/edit#gid=1310233339

    The ID falls between the /d and /edit

    1iTRfuFTPidnJoplKVH4e5znlk3my
    ```

    Sample Google sheet:
    ```
    host,os,ansible_user,ansible_password,ansible_become_pass,site,groups
    nxos101,nxos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,red blue
    nxos102,nxos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,blue yellow
    nxos103,nxos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,red blue
    nxos104,nxos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,blue yellow
    eos10[1:4],eos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,orange red
    vyos10[1:4],vyos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,orange red
    ```


6) Define a `nmake_inventory_gsheet.yaml` file:

    Note:

    - The credentials key should point to the credentials file downloaded above
    - The token should point ot the token file created above

    ```yaml
    plugin: nmake.inventory.gsheet
    credentials: /home/username/credentials.json
    token: /home/username/token.pickle
    sheet_id: 1iTRfuFTPidnJoplKVH4e5znlk3my


    # add an attribute to each host based on a conditional
    compose:
      ansible_become: ansible_network_os == "eos"
      ansible_python_interpreter: python

    # build dynamic groups based on csv columns
    keyed_groups:
      - key: site
        prefix: site
      - key: ansible_network_os
        prefix: ""
        separator: ""

    # allow the csv to contain `vars:xxx` values which reference these
    vars:
      ansible_user: "{{ lookup('env', 'ansible_user') }}"
      ansible_password: "{{ lookup('env', 'ansible_password') }}"
      ansible_become_pass: "{{ lookup('env', 'ansible_become_pass') }}"

    # add an attribute to each host if it's not in the csv
    defaults:
      ansible_become_method: enable
      ansible_connection: network_cli
      ansible_python_interpreter: python


    # in case the CSV columns don't match what we need
    column_replace:
      os: ansible_network_os
    ```

7) Update the ansible.cfg file to allow the CSV inventory plugin:

    ```ini
    [inventory]
    enable_plugins = nmake.inventory.gsheet
    ```

8) Check the inventory

    ```bash
    ansible-inventory -i nmake_inventory_gsheet.yaml --list
    ```

    ```json
    {
        "_meta": {
            "hostvars": {
                "eos101": {
                    "ansible_become": true,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "eos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "eos102": {
                    "ansible_become": true,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "eos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "eos103": {
                    "ansible_become": true,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "eos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "eos104": {
                    "ansible_become": true,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "eos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "nxos101": {
                    "ansible_become": false,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "nxos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "nxos102": {
                    "ansible_become": false,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "nxos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "nxos103": {
                    "ansible_become": false,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "nxos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "nxos104": {
                    "ansible_become": false,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "nxos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "vyos101": {
                    "ansible_become": false,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "vyos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "vyos102": {
                    "ansible_become": false,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "vyos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "vyos103": {
                    "ansible_become": false,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "vyos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                },
                "vyos104": {
                    "ansible_become": false,
                    "ansible_become_method": "enable",
                    "ansible_become_pass": "{{ lookup('env', 'ansible_become_pass') }}",
                    "ansible_connection": "network_cli",
                    "ansible_network_os": "vyos",
                    "ansible_password": "{{ lookup('env', 'ansible_password') }}",
                    "ansible_python_interpreter": "python",
                    "ansible_user": "{{ lookup('env', 'ansible_user') }}",
                    "site": "my_lab"
                }
            }
        },
        "all": {
            "children": [
                "blue",
                "eos",
                "nxos",
                "orange",
                "red",
                "site_my_lab",
                "ungrouped",
                "vyos",
                "yellow"
            ]
        },
        "blue": {
            "hosts": [
                "nxos101",
                "nxos102",
                "nxos103",
                "nxos104"
            ]
        },
        "eos": {
            "hosts": [
                "eos101",
                "eos102",
                "eos103",
                "eos104"
            ]
        },
        "nxos": {
            "hosts": [
                "nxos101",
                "nxos102",
                "nxos103",
                "nxos104"
            ]
        },
        "orange": {
            "hosts": [
                "eos101",
                "eos102",
                "eos103",
                "eos104",
                "vyos101",
                "vyos102",
                "vyos103",
                "vyos104"
            ]
        },
        "red": {
            "hosts": [
                "eos101",
                "eos102",
                "eos103",
                "eos104",
                "nxos101",
                "nxos103",
                "vyos101",
                "vyos102",
                "vyos103",
                "vyos104"
            ]
        },
        "site_my_lab": {
            "hosts": [
                "eos101",
                "eos102",
                "eos103",
                "eos104",
                "nxos101",
                "nxos102",
                "nxos103",
                "nxos104",
                "vyos101",
                "vyos102",
                "vyos103",
                "vyos104"
            ]
        },
        "vyos": {
            "hosts": [
                "vyos101",
                "vyos102",
                "vyos103",
                "vyos104"
            ]
        },
        "yellow": {
            "hosts": [
                "nxos102",
                "nxos104"
            ]
        }
    }
    ```

9) Run ansible:

    ```yaml
    # site.yaml
    - hosts: all
      gather_facts: False
      tasks:
      - name: Use the platform facts module for each
        action: "{{ ansible_network_os }}_facts"
        args:
          gather_network_resources:
          - interfaces
      - debug:
          msg: "{{ hostvars[inventory_hostname] }}"
    ```

    ```shell
    ansible-playbook -i nmake_inventory_gsheet.yaml site.yaml
    ```

from ansible.plugins.inventory import (
    BaseInventoryPlugin,
    Constructable,
    expand_hostname_range,
    detect_range,
)

import pickle
import os.path
from ansible.errors import AnsibleError

try:
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
except ImportError:
    raise AnsibleError(
        "This inventory requires several python libraries that appear to be missing `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`"
    )

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


DOCUMENTATION = """
    name: name.inventory.gsheet
    plugin_type: inventory
    short_description: Use a Google sheet as an inventory source
    description:
        - Use a Google sheet as an inventory source
    extends_documentation_fragment:
      - constructed
    options:
        column_replace:
            description: Replace a column name in the csv with an alternate name
            type: dict
        credentials:
            description: The full path to the credentials.json file
            type: str
            required: True
        defaults:
            description: Assign attributes to hosts when not in the CSV file
            type: dict
        plugin:
            description: token that ensures this is a source file for the 'csv' plugin
            required: True
            choices: ['nmake.inventory.gsheet']
        sheet_id:
            description: The ID for the google sheet from the sheet's URL
            required: True
        token:
            description: The full path to the token file
            required: True
            type: str
        vars:
            description: Use variables to provide CSV values
            type: dict
"""
EXAMPLES = """
# sample gsheet file
# host,os,ansible_user,ansible_password,ansible_become_pass,site,groups
# nxos101,nxos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,red blue
# nxos102,nxos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,blue yellow
# nxos103,nxos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,red blue
# nxos104,nxos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,blue yellow
# eos10[1:4],eos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,orange red
# vyos10[1:4],vyos,vars:ansible_user,vars:ansible_password,vars:ansible_become_pass,my_lab,orange red


# nmake_inventory_gsheet.yaml

plugin: nmake.inventory.gsheet
credentials: /home/username/credentials.json
token: /home/username/token.pickle
sheet_id: 1iTRfuFTPidnJoplKVH4e5znlk3my

# add an attribute to each host based on a conditional
compose:
  ansible_become: ansible_network_os == "eos"

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
  ansible_connection: network_cli

# in case the CSV columns don't match what we need
column_replace:
  os: ansible_network_os
 """


def get_creds(token_path, cred_path):
    creds = None

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, "wb") as token:
            pickle.dump(creds, token)
    return creds


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Ansible Google sheet inventory"
    )
    parser.add_argument("--token", type=str, help="Full path for token file")
    parser.add_argument(
        "--credentials", type=str, help="Full path to credentials.json"
    )
    args = parser.parse_args()
    creds = get_creds(args.token, args.credentials)
    if creds:
        print("{} created successfully".format(args.token))


class InventoryModule(BaseInventoryPlugin, Constructable):

    NAME = "nmake.inventory.gsheet"

    def verify_file(self, path):
        """ return true/false if this is possibly a valid file for this plugin to consume """
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(
                ("nmake_inventory_gsheet.yaml", "nmake_inventory_gsheet.yml")
            ):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        config = self._read_config_data(path)
        cred_path = self.get_option("credentials")
        sheet_id = self.get_option("sheet_id")
        token = self.get_option("token")

        creds = get_creds(token, cred_path)

        service = build("sheets", "v4", credentials=creds)

        sheet = service.spreadsheets()
        sheet_metadata = (
            service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        )
        properties = sheet_metadata.get("sheets")
        rows = properties[0]["properties"]["gridProperties"]["rowCount"]
        columns = properties[0]["properties"]["gridProperties"]["columnCount"]
        range_name = "R1C1:R{}C{}".format(rows, columns)

        result = (
            sheet.values()
            .get(spreadsheetId=sheet_id, range=range_name)
            .execute()
        )
        values = result.get("values", [])
        dicts = [dict(zip(values[0], row)) for row in values[1:]]
        self.add_to_inventory(dicts, config)

    def add_to_inventory(self, list_of_dicts, config):
        strict = self.get_option("strict")
        for entry in list_of_dicts:
            hostvars = {}
            groups = []

            if detect_range(entry["host"]):
                hosts = expand_hostname_range(entry["host"])
            else:
                hosts = [entry["host"]]

            for host in hosts:
                self.inventory.add_host(host)
                for k, v in entry.items():
                    if k not in ["host", "tags"]:
                        if v.startswith("vars:"):
                            varval = v.split("vars:")[1]
                            v = config["vars"].get(varval)
                        if k in config.get("column_replace", {}):
                            add_key = config["column_replace"][k]
                        else:
                            add_key = k
                        hostvars[add_key] = v
                    if k == "groups":
                        groups = v.split(" ")

                for k, v in config.get("defaults", {}).items():
                    if k not in hostvars:
                        hostvars[k] = v

                for k, v in hostvars.items():
                    self.inventory.set_variable(host, k, v)

                self._set_composite_vars(
                    self.get_option("compose"), hostvars, host, strict=strict
                )
                self._add_host_to_composed_groups(
                    self.get_option("groups"), hostvars, host, strict=strict
                )
                self._add_host_to_keyed_groups(
                    self.get_option("keyed_groups"),
                    hostvars,
                    host,
                    strict=strict,
                )

                for group in groups:
                    self.inventory.add_group(group=group)
                    self.inventory.add_host(group=group, host=host)


if __name__ == "__main__":
    main()

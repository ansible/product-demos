#!/usr/bin/python
"""Read only the Junos routing configuration needed by the network report."""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection, ConnectionError

DOCUMENTATION = r"""
---
module: junos_route_configuration
short_description: Read filtered Junos route configuration over NETCONF
description:
  - Reads routing options and routing instances from the running configuration.
  - Uses the Junos NETCONF connection without modifying device configuration.
author: Ansible Product Demos
"""

EXAMPLES = r"""
- name: Read route configuration
  demo.network.junos_route_configuration:
  register: route_configuration
"""

RETURN = r"""
xml:
  description: Filtered route configuration XML for report normalization.
  returned: success
  type: str
"""

FILTER = "<configuration><routing-options/><routing-instances/></configuration>"


def main():
    module = AnsibleModule(argument_spec={}, supports_check_mode=True)
    if not module._socket_path:
        module.fail_json(msg="This module requires a Junos NETCONF connection")
    try:
        response = Connection(module._socket_path).get_configuration(filter=FILTER)
    except ConnectionError as exc:
        module.fail_json(msg=str(exc))
    module.exit_json(changed=False, xml=response)


if __name__ == "__main__":
    main()

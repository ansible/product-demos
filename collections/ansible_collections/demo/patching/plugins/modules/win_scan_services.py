#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: win_scan_services
short_description: Return service state information as fact data
description:
     - Return service state information as fact data for various service management utilities
'''

EXAMPLES = '''
- monit: win_scan_services
# Example fact output:
# host | success >> {
#    "ansible_facts": {
#	"services": [
            {
                "name": "AllJoyn Router Service",
                "win_svc_name": "AJRouter",
                "state": "stopped"
            },
            {
                "name": "Application Layer Gateway Service",
                "win_svc_name": "ALG",
                "state": "stopped"
            },
            {
                "name": "Application Host Helper Service",
                "win_svc_name": "AppHostSvc",
                "state": "running"
            },
#   }
'''
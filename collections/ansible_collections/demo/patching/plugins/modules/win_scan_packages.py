#!/usr/bin/env python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: win_scan_packages
short_description: Return Package state information as fact data
description:
     - Return Package state information as fact data for various Packages
'''

EXAMPLES = '''
- monit: win_scan_packages
# Example fact output:
# host | success >> {
#    "ansible_facts": {
#	"packages": [
            {
                "name": "Mozilla Firefox 76.0.1 (x64 en-US)",
                "version": "76.0.1",
                "publisher": "Mozilla",
                "arch": "Win64"
            },
            {
                "name": "Mozilla Maintenance Service",
                "version": "76.0.1",
                "publisher": "Mozilla",
                "arch": "Win64"
            },
#   }
'''
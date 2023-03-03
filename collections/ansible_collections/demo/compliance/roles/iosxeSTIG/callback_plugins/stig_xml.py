from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.callback import CallbackBase
from time import gmtime, strftime
import platform
import tempfile
import re
import sys
import os
import json
import xml.etree.ElementTree as ET
import xml.dom.minidom

role = "iosxeSTIG"

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'xml'
    CALLBACK_NAME = 'stig_xml'

    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.rules = {}
        self.stig_path = os.environ.get('STIG_PATH')
        self.XML_path = os.environ.get('XML_PATH')
        if self.stig_path is None:
            self.stig_path = os.path.join(os.getcwd(), "roles", role, "files")
            self._display.display('Using STIG_PATH: {}'.format(self.stig_path))
        if self.XML_path is None:
            self.XML_path = os.getcwd()
            self._display.display('Using XML_PATH: {}'.format(self.XML_path))

        print("Writing: {}".format(self.XML_path))
        STIG_name = os.path.basename(self.stig_path)
        ET.register_namespace('cdf', 'http://checklists.nist.gov/xccdf/1.2')
        self.tr = ET.Element('{http://checklists.nist.gov/xccdf/1.2}TestResult')
        self.tr.set('id', 'xccdf_mil.disa.stig_testresult_scap_mil.disa_comp_{}'.format(STIG_name))
        endtime = strftime("%Y-%m-%dT%H:%M:%S", gmtime())
        self.tr.set('end-time', endtime)
        tg = ET.SubElement(self.tr, '{http://checklists.nist.gov/xccdf/1.2}target')
        tg.text = platform.node()

    def __get_rev(self, nid):
        rev = '0'
        # Check all files for the rule number.
        for file in os.listdir(self.stig_path):
            with open(os.path.join(self.stig_path, file), 'r') as f:
                r = 'SV-{}r(?P<rev>\d)_rule'.format(nid)
                m = re.search(r, f.read())
            if m:
                rev = m.group('rev')
                break
        return rev

    def v2_runner_on_ok(self, result):
        name = result._task.get_name()
        m = re.search('stigrule_(?P<id>\d+)', name)
        if m:
            nid = m.group('id')
        else:
            return
        rev = self.__get_rev(nid)
        key = "{}r{}".format(nid, rev)
        if self.rules.get(key, 'Unknown') != False:
            self.rules[key] = result.is_changed()

    def __set_duplicates(self):
        with open(os.path.join(self.stig_path, 'duplicates.json')) as f:
            dups = json.load(f)
        for d in dups:
            dup_of = str(dups[d][0])
            rev = self.__get_rev(d)
            key = "{}r{}".format(d, rev)
            dup_of_rev = self.__get_rev(dup_of)
            dup_of_key = "{}r{}".format(dup_of, dup_of_rev)
            if dup_of_key in self.rules:
                self.rules[key] = self.rules[dup_of_key]

    def v2_playbook_on_stats(self, stats):
        self.__set_duplicates()
        for rule, changed in self.rules.items():
            state = 'fail' if changed else 'pass'
            rr = ET.SubElement(self.tr, '{http://checklists.nist.gov/xccdf/1.2}rule-result')
            rr.set('idref', 'xccdf_mil.disa.stig_rule_SV-{}_rule'.format(rule))
            rs = ET.SubElement(rr, '{http://checklists.nist.gov/xccdf/1.2}result')
            rs.text = state
        passing = len(self.rules) - sum(self.rules.values())
        sc = ET.SubElement(self.tr, '{http://checklists.nist.gov/xccdf/1.2}score')
        sc.set('maximum', str(len(self.rules)))
        sc.set('system', 'urn:xccdf:scoring:flat-unweighted')
        sc.text = str(passing)
        with open(os.path.join(self.XML_path, "xccdf-results.xml"), 'w') as f:
            out = ET.tostring(self.tr)
            pretty = xml.dom.minidom.parseString(out).toprettyxml(encoding='utf-8')
            f.write(pretty)

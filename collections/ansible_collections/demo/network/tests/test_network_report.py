"""Offline coverage of vendor schemas, partial collection, and report publication."""

import importlib.util
import json
from pathlib import Path
import unittest

from jinja2 import Environment, StrictUndefined

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "network_report", ROOT / "plugins/filter/network_report.py"
)
REPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT)


def device_fixture(
    name="vjunos", vendor="Juniper", os="Junos", network_os="juniper.device.junos"
):
    base = {
        "ansible_facts": {
            "ansible_net_hostname": name,
            "ansible_net_version": "25.2R1.9",
            "ansible_net_model": "EX9214",
            "ansible_net_serialnum": "LAB-001",
            "available_network_resources": [
                "interfaces",
                "l3_interfaces",
                "vlans",
                "lldp_interfaces",
                "bgp_global",
            ],
        }
    }
    legacy = {
        "results": [
            {
                "item": "interfaces",
                "ansible_facts": {
                    "ansible_net_interfaces": {
                        "ge-0/0/0": {
                            "oper-status": "up",
                            "admin-status": "up",
                            "mtu": "1514",
                            "speed": "1Gbps",
                        }
                    },
                },
            },
            {"item": "hardware", "ansible_facts": {"ansible_net_memtotal_mb": 5120}},
        ]
    }
    resources = {
        "results": [
            {
                "item": "interfaces",
                "ansible_facts": {
                    "ansible_network_resources": {
                        "interfaces": [{"name": "ge-0/0/0", "enabled": True}]
                    }
                },
            },
            {
                "item": "l3_interfaces",
                "ansible_facts": {
                    "ansible_network_resources": {
                        "l3_interfaces": [
                            {
                                "name": "irb",
                                "unit": 110,
                                "ipv4": [{"address": "10.110.0.2/24"}],
                            }
                        ]
                    }
                },
            },
            {
                "item": "vlans",
                "ansible_facts": {"ansible_network_resources": {"vlans": []}},
            },
            {
                "item": "lldp_interfaces",
                "ansible_facts": {
                    "ansible_network_resources": {
                        "lldp_interfaces": [{"name": "ge-0/0/0", "enabled": True}]
                    }
                },
            },
            {
                "item": "bgp_global",
                "failed": True,
                "msg": "Parser did not recognize this configuration",
            },
        ]
    }
    neighbors = {
        "output": [
            {
                "lldp-neighbors-information": [
                    {
                        "lldp-neighbor-information": [
                            {
                                "lldp-local-interface": [{"data": "ge-0/0/0"}],
                                "lldp-remote-system-name": [{"data": "n9kv"}],
                                "lldp-remote-port-id": [{"data": "Ethernet1/2"}],
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return dict(
        name=name,
        address="192.0.2.10",
        port=2830,
        network_os=network_os,
        connection="ansible.netcommon.netconf",
        platform={
            "vendor": vendor,
            "os": os,
            "facts_module": "juniper.device.junos_facts",
        },
        base=base,
        legacy=legacy,
        resource_results=resources,
        neighbor_result=neighbors,
        requested_resources=[
            "interfaces",
            "l3_interfaces",
            "vlans",
            "lldp_interfaces",
            "bgp_global",
            "ospfv2",
        ],
    )


class NetworkReportTests(unittest.TestCase):
    def test_junos_ipv4_management_vrf_without_ipv6_rib(self):
        result = REPORT.network_report_junos_static_routes(
            {
                "xml": (
                    '<rpc-reply xmlns="urn:test"><configuration><routing-options><static>'
                    "<route><name>0.0.0.0/0</name><next-hop>10.0.0.2</next-hop></route>"
                    "</static></routing-options>"
                    "<routing-instances><instance><name>mgmt_junos</name>"
                    "<routing-options><static><route><name>0.0.0.0/0</name>"
                    "<next-hop>10.0.0.2</next-hop></route></static></routing-options>"
                    "</instance></routing-instances></configuration></rpc-reply>"
                )
            }
        )
        routes = result["ansible_facts"]["ansible_network_resources"]["static_routes"]
        self.assertNotIn("failed", result)
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[1]["vrf"], "mgmt_junos")
        self.assertEqual(
            routes[1]["address_families"][0]["routes"][0],
            {"dest": "0.0.0.0/0", "next_hop": [{"forward_router_address": "10.0.0.2"}]},
        )

    def test_junos_multiple_instances_and_ipv6_routes(self):
        result = REPORT.network_report_junos_static_routes(
            {
                "stdout": [
                    "<configuration><routing-options><rib><name>inet6.0</name><static>"
                    "<route><name>::/0</name><next-hop>2001:db8::1</next-hop></route>"
                    "</static></rib></routing-options></configuration>",
                    "<configuration><routing-instances>"
                    "<instance><name>empty</name></instance>"
                    "<instance><name>blue</name><routing-options><rib><name>blue.inet6.0</name>"
                    "<static><route><name>2001:db8:2::/64</name><discard/></route></static>"
                    "</rib></routing-options></instance></routing-instances></configuration>",
                ]
            }
        )
        routes = result["ansible_facts"]["ansible_network_resources"]["static_routes"]
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0]["address_families"][0]["afi"], "ipv6")
        self.assertEqual(routes[1]["vrf"], "blue")
        self.assertTrue(routes[1]["address_families"][0]["routes"][0]["discard"])

    def test_junos_empty_static_routes_are_unconfigured(self):
        result = REPORT.network_report_junos_static_routes(
            {"stdout": ["<configuration/>", "<configuration/>"]}
        )
        fixture = device_fixture()
        fixture["base"]["ansible_facts"]["available_network_resources"].append(
            "static_routes"
        )
        fixture["requested_resources"] = ["static_routes"]
        fixture["resource_results"] = {"results": [result]}
        device = REPORT.network_report_device(**fixture)
        self.assertEqual(device["status"], "collected")
        self.assertEqual(device["sections"][0]["status"], "not configured")

    def test_junos_route_transport_errors_remain_failures(self):
        for failure in ({"failed": True}, {"unreachable": True}):
            result = REPORT.network_report_junos_static_routes(
                {**failure, "msg": "Connection closed"}
            )
            self.assertTrue(result["failed"])
            self.assertEqual(result["msg"], "Connection closed")

    def test_junos_invalid_rpc_responses_remain_failures(self):
        for responses in (
            [],
            ["not xml", "<configuration/>"],
            ["<rpc-reply><rpc-error/></rpc-reply>", "<configuration/>"],
            ["<rpc-reply/>", "<configuration/>"],
            [
                "<configuration><routing-options><static><route/></static></routing-options></configuration>",
                "<configuration/>",
            ],
        ):
            with self.subTest(responses=responses):
                result = REPORT.network_report_junos_static_routes(
                    {"stdout": responses}
                )
                self.assertTrue(result["failed"])
                self.assertNotIn("ansible_facts", result)

    def test_document_counts_partial_failed_and_missing_devices(self):
        partial = REPORT.network_report_device(**device_fixture())
        failed = REPORT.network_report_device(
            **{
                **device_fixture(name="offline"),
                "base": {"failed": True, "msg": "Authentication failed"},
                "legacy": {},
                "resource_results": {},
                "neighbor_result": {},
            }
        )
        report = REPORT.network_report_document(
            {
                "partial": {"network_report_device": partial},
                "failed": {"network_report_device": failed},
                "missing": {},
            },
            ["partial", "failed", "missing"],
            "now",
        )
        self.assertEqual(report["issue_count"], 3)
        self.assertEqual(report["complete_count"], 0)

    def test_successful_empty_resource_mapping_is_unconfigured(self):
        fixture = device_fixture()
        fixture["resource_results"]["results"][2]["ansible_facts"] = {
            "ansible_network_resources": {}
        }
        device = REPORT.network_report_device(**fixture)
        self.assertEqual(device["sections"][2]["status"], "not configured")

    def test_missing_resource_mapping_is_a_collection_issue(self):
        fixture = device_fixture()
        fixture["resource_results"]["results"][2]["ansible_facts"] = {}
        device = REPORT.network_report_device(**fixture)
        self.assertEqual(device["sections"][2]["status"], "not collected")

    def test_junos_units_and_operational_state(self):
        device = REPORT.network_report_device(**device_fixture())
        self.assertEqual(device["interfaces"][0]["operational"], "up")
        self.assertEqual(device["sections"][1]["rows"][0]["unit"], 110)
        self.assertEqual(device["neighbors"][0]["neighbor"], "n9kv")

    def test_junos_25_local_port_identifier(self):
        fixture = device_fixture()
        entry = fixture["neighbor_result"]["output"][0]["lldp-neighbors-information"][
            0
        ]["lldp-neighbor-information"][0]
        entry["lldp-local-port-id"] = entry.pop("lldp-local-interface")
        device = REPORT.network_report_device(**fixture)
        self.assertEqual(device["neighbors"][0]["local_interface"], "ge-0/0/0")

    def test_partial_failure_preserves_device_and_other_sections(self):
        device = REPORT.network_report_device(**device_fixture())
        self.assertEqual(device["status"], "partial")
        self.assertEqual(device["hostname"], "vjunos")
        statuses = {s["name"]: s["status"] for s in device["sections"]}
        self.assertEqual(statuses["vlans"], "not configured")
        self.assertEqual(statuses["bgp_global"], "failed")
        self.assertEqual(statuses["ospfv2"], "unsupported")
        self.assertEqual(statuses["lldp_interfaces"], "collected")

    def test_unreachable_device_is_retained(self):
        fixture = device_fixture()
        fixture.update(
            base={"unreachable": True, "msg": "Connection refused"},
            legacy={},
            resource_results={},
            neighbor_result={},
        )
        device = REPORT.network_report_device(**fixture)
        self.assertEqual(device["status"], "failed")
        self.assertTrue(all(s["status"] == "not collected" for s in device["sections"]))
        self.assertEqual(device["name"], "vjunos")

    def test_only_this_jobs_selected_hosts_are_published(self):
        device = REPORT.network_report_device(**device_fixture())
        report = REPORT.network_report_document(
            {
                "vjunos": {"network_report_device": device},
                "veos": {"network_report_device": {"password": "never published"}},
            },
            ["vjunos"],
            "now",
        )
        self.assertEqual(len(report["devices"]), 1)
        self.assertNotIn("never published", json.dumps(report))

    def test_missing_collection_still_has_a_report_row(self):
        report = REPORT.network_report_document({"offline": {}}, ["offline"], "now")
        self.assertEqual(report["devices"][0]["status"], "not collected")
        self.assertEqual(report["issue_count"], 1)

    def test_secrets_and_raw_hostvars_are_excluded(self):
        fixture = device_fixture()
        fixture["secrets"] = ["sensitive-demo-value"]
        fixture["base"]["ansible_facts"][
            "ansible_net_config"
        ] = "PRIVATE RUNNING CONFIG"
        fixture["resource_results"]["results"].append(
            {
                "item": "bgp_global",
                "ansible_facts": {
                    "ansible_network_resources": {
                        "bgp_global": {
                            "neighbors": [
                                {
                                    "password": "sensitive-demo-value",
                                    "description": "sensitive-demo-value",
                                }
                            ]
                        }
                    }
                },
            }
        )
        serialized = json.dumps(REPORT.network_report_device(**fixture))
        self.assertNotIn("sensitive-demo-value", serialized)
        self.assertNotIn("PRIVATE RUNNING CONFIG", serialized)
        self.assertIn("[redacted]", serialized)

    def test_html_escapes_device_strings(self):
        fixture = device_fixture(name='<script>alert("device")</script>')
        device = REPORT.network_report_device(**fixture)
        env = Environment(undefined=StrictUndefined, autoescape=False)
        env.filters["demo.network.network_report_cell"] = REPORT.network_report_cell
        template = env.from_string(
            (ROOT / "roles/build_report/templates/report.html.j2").read_text()
        )
        html = template.render(
            network_report={
                "devices": [device],
                "generated_at": "Fixture preview",
                "vendor_count": 1,
                "complete_count": 0,
                "issue_count": 1,
            }
        )
        self.assertNotIn('<script>alert("device")</script>', html)
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn('src="http', html)

    def test_cisco_and_eos_legacy_neighbor_schemas(self):
        for network_os in ["cisco.ios.ios", "cisco.nxos.nxos", "arista.eos.eos"]:
            with self.subTest(network_os=network_os):
                fixture = device_fixture(network_os=network_os)
                fixture["legacy"]["results"][0]["ansible_facts"] = {
                    "ansible_net_interfaces": {
                        "Ethernet1": {
                            "lineprotocol": "up",
                            "macaddress": "00:00:5e:00:53:01",
                        }
                    },
                    "ansible_net_neighbors": {
                        "Ethernet1": [{"host": "peer", "port": "ge-0/0/0"}]
                    },
                }
                d = REPORT.network_report_device(**fixture)
                self.assertEqual(d["neighbors"][0]["neighbor"], "peer")
                self.assertEqual(d["interfaces"][0]["operational"], "up")
                self.assertEqual(d["neighbor_status"], "collected")

    def test_nxos_state_is_an_operational_observation(self):
        fixture = device_fixture(network_os="cisco.nxos.nxos")
        fixture["legacy"]["results"][0]["ansible_facts"] = {
            "ansible_net_interfaces": {
                "Ethernet1/1": {"state": "up", "speed": "1000 Mb/s"}
            }
        }
        device = REPORT.network_report_device(**fixture)
        self.assertEqual(device["interfaces"][0]["operational"], "up")

    def test_omitted_supported_resource_is_a_collection_issue(self):
        fixture = device_fixture()
        fixture["resource_results"]["results"] = []
        device = REPORT.network_report_device(**fixture)
        self.assertEqual(device["status"], "partial")
        self.assertTrue(
            any(error["section"] == "interfaces" for error in device["errors"])
        )

    def test_unsupported_platform_has_an_explicit_status(self):
        fixture = device_fixture()
        fixture.update(
            platform={}, base={}, legacy={}, resource_results={}, neighbor_result={}
        )
        self.assertEqual(
            REPORT.network_report_device(**fixture)["status"], "unsupported"
        )


if __name__ == "__main__":
    unittest.main()

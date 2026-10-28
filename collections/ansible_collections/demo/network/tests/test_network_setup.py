"""Check Controller survey targets and connection mappings without creating jobs."""

from pathlib import Path
import unittest

import yaml

REPO = Path(__file__).resolve().parents[5]


class SetupLoader(yaml.SafeLoader):
    """Preserve Controller's deferred Jinja strings without evaluating lookups."""


SetupLoader.add_constructor(
    "!unsafe", lambda loader, node: loader.construct_scalar(node)
)


class NetworkSetupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.setup = yaml.load(
            (REPO / "network/setup.yml").read_text(), Loader=SetupLoader
        )
        cls.defaults = yaml.safe_load(
            (
                REPO
                / "collections/ansible_collections/demo/network/roles/containerlab/defaults/main.yml"
            ).read_text()
        )

    def test_device_surveys_only_offer_existing_inventory_targets(self):
        groups = {
            group["name"]
            for group in self.setup["controller_groups"]
            if group.get("state", "present") != "absent"
        }
        targets = groups | {host["name"] for host in self.setup["controller_hosts"]}
        surveys = 0
        for template in self.setup["controller_templates"]:
            for question in template.get("survey", {}).get("spec", []):
                if question["variable"] == "_hosts":
                    with self.subTest(template=template["name"]):
                        self.assertTrue(set(question["choices"]) <= targets)
                        self.assertIn(question["default"], question["choices"])
                    surveys += 1
        self.assertGreater(surveys, 0)

    def test_management_cidr_is_prompted_for_every_deployment_entrypoint(self):
        names = {
            "NETWORK | Containerlab | Provision Hypervisor",
            "NETWORK | Containerlab | Deploy Topology",
            "NETWORK | Deploy Containerlab Stack",
        }
        templates = (
            self.setup["controller_templates"] + self.setup["controller_workflows"]
        )
        found = set()
        for template in templates:
            if template["name"] not in names:
                continue
            questions = template["survey"]["spec"]
            cidr = [q for q in questions if q["variable"] == "clab_access_cidr"]
            with self.subTest(template=template["name"]):
                self.assertEqual(len(cidr), 1)
                self.assertTrue(cidr[0]["required"])
                self.assertEqual(cidr[0]["type"], "text")
                self.assertEqual(cidr[0]["default"], self.defaults["clab_access_cidr"])
            found.add(template["name"])
        self.assertEqual(found, names)

    def test_instance_surveys_match_the_role_default(self):
        templates = (
            self.setup["controller_templates"] + self.setup["controller_workflows"]
        )
        for template in templates:
            for question in template.get("survey", {}).get("spec", []):
                if question["variable"] == "clab_aws_instance_type":
                    with self.subTest(template=template["name"]):
                        self.assertEqual(
                            question["default"], self.defaults["clab_aws_instance_type"]
                        )

    def test_setup_inventory_matches_the_deployed_device_catalog(self):
        catalog = self.defaults["clab_device_catalog"]
        groups = {group["name"]: group for group in self.setup["controller_groups"]}
        self.assertEqual(
            {host["name"] for host in self.setup["controller_hosts"]}, set(catalog)
        )
        for name, device in catalog.items():
            with self.subTest(device=name):
                group = groups[device["group"]]
                self.assertIn(name, group["hosts"])
                self.assertEqual(
                    group["variables"]["ansible_network_os"], device["network_os"]
                )

    def test_every_catalog_platform_has_a_validation_command_module(self):
        plays = yaml.safe_load((REPO / "network/validate_containerlab.yml").read_text())
        modules = plays[1]["vars"]["clab_validation_command_modules"]
        for device in self.defaults["clab_device_catalog"].values():
            with self.subTest(platform=device["network_os"]):
                self.assertIn(device["network_os"], modules)
                self.assertTrue(modules[device["network_os"]].endswith("_command"))


if __name__ == "__main__":
    unittest.main()

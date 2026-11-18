"""Exercise route-table selection with Ansible and fixture AWS responses."""

import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

SOURCE = Path(__file__).resolve().parents[1] / "create_vpc.yml"


class RouteTableSelection(unittest.TestCase):
    def run_case(
        self,
        tables,
        expected=None,
        success=True,
        error="Multiple demo route tables exist",
    ):
        play = yaml.safe_load(SOURCE.read_text())[0]
        names = [
            "Select non-main route tables",
            "Find a demo route table already associated with the subnet",
            "Reject ambiguous demo route tables",
            "Reject a matching main table when no reusable table exists",
            "Select the demo route table to reuse",
        ]
        tasks = [task for task in play["tasks"] if task["name"] in names]
        tasks.insert(
            0,
            {
                "name": "Set fixture results",
                "ansible.builtin.set_fact": {
                    "aws_named_route_tables": {"route_tables": tables},
                    "aws_subnet": {"subnet": {"id": "subnet-test"}},
                },
            },
        )
        tasks.append(
            {
                "name": "Report selected table",
                "ansible.builtin.debug": {
                    "msg": "SELECTED={{ aws_reusable_route_table.id | default('new') }}"
                },
            }
        )
        with tempfile.TemporaryDirectory(prefix="route-test-") as tmp:
            path = Path(tmp) / "test.yml"
            path.write_text(
                yaml.safe_dump(
                    [
                        {
                            "name": "Test route selection",
                            "hosts": "localhost",
                            "gather_facts": False,
                            "tasks": tasks,
                        }
                    ],
                    sort_keys=False,
                )
            )
            result = subprocess.run(
                ["ansible-playbook", "-i", "localhost,", "-c", "local", str(path)],
                text=True,
                capture_output=True,
                timeout=60,
            )
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode == 0, success, output)
        if success:
            self.assertIn(f"SELECTED={expected}", output)
        else:
            self.assertIn(error, output)

    def test_new_table_when_none_exists(self):
        self.run_case([], "new")

    def test_single_table_is_reused_despite_owner_change(self):
        self.run_case(
            [{"id": "rtb-old", "tags": {"owner": "other"}, "associations": []}],
            "rtb-old",
        )

    def test_associated_table_wins_among_duplicates(self):
        self.run_case(
            [
                {"id": "rtb-one", "associations": []},
                {
                    "id": "rtb-two",
                    "associations": [{"main": False, "subnet_id": "subnet-test"}],
                },
            ],
            "rtb-two",
        )

    def test_ambiguous_unassociated_tables_fail(self):
        self.run_case(
            [
                {"id": "rtb-one", "associations": []},
                {"id": "rtb-two", "associations": []},
            ],
            success=False,
        )

    def test_main_route_table_is_not_selected(self):
        self.run_case(
            [{"id": "rtb-main", "associations": [{"main": True}]}],
            success=False,
            error="A matching main route table exists",
        )


if __name__ == "__main__":
    unittest.main()

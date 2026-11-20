"""Exercise the Install job's workaround tasks using a Kubernetes CLI double."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT.parent / "install.yml"
ORIGINAL = "class GenericAgent:\n    async def _execute_structured(self, state, response_schema):\n        return state\n"
SOURCE_HASH = "e7f21a189bf9863a0a0b1d756cdcb0e28eaa1b2c932168923ca0b6229996344f"
OVERLAY_HASH = "d78d4ab4734d0b9c82a5e7b908722617ed5dfdc13ad1bfb98ff205a20ace4342"
IMAGE = "registry.example/backend@sha256:22279cf11cc61116e4eb5b67d3479d011af668708effe74203913071dcc99f14"


class RolloutTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ao-rollout-test-")
        self.path = Path(self.tmp.name)
        scripts = self.path / "scripts"
        scripts.mkdir()
        shutil.copy(ROOT / "structured_method.py.txt", scripts)
        manager = scripts / "manage_overlay.py"
        fragment = (scripts / "structured_method.py.txt").read_text()
        lines = ORIGINAL.splitlines(keepends=True)
        original_method = "".join(lines[1:]).replace(
            "async def _execute_structured(", "async def _execute_structured_native(", 1
        )
        overlay = lines[0] + fragment + "\n\n" + original_method
        manager.write_text(
            (ROOT / "manage_overlay.py")
            .read_text()
            .replace(SOURCE_HASH, hashlib.sha256(ORIGINAL.encode()).hexdigest())
            .replace(OVERLAY_HASH, hashlib.sha256(overlay.encode()).hexdigest())
        )
        bindir = self.path / "bin"
        bindir.mkdir()
        (bindir / "kubectl").symlink_to(ROOT / "tests" / "fake_kubectl.py")
        self.state = self.path / "state.json"
        self.state.write_text(
            json.dumps(
                {
                    "original": ORIGINAL,
                    "configmap": None,
                    "deployment": {
                        "metadata": {
                            "name": "automation-orchestrator-background-worker",
                            "resourceVersion": "1",
                        },
                        "spec": {
                            "replicas": 1,
                            "selector": {"matchLabels": {"app": "bg"}},
                            "template": {
                                "spec": {
                                    "volumes": [{"name": "existing"}],
                                    "containers": [
                                        {
                                            "name": "background-worker",
                                            "image": IMAGE,
                                            "volumeMounts": [
                                                {
                                                    "name": "existing",
                                                    "mountPath": "/existing",
                                                }
                                            ],
                                        }
                                    ],
                                }
                            },
                        },
                    },
                }
            )
        )
        plays = yaml.safe_load(INSTALL.read_text())
        block = next(
            task["block"]
            for task in plays[0]["tasks"]
            if task["name"] == "Deploy Automation Orchestrator"
        )
        names = {
            "Validate the AO structured-output workaround state",
            "Wait for the AO background worker",
            "Manage the AO structured-output workaround",
        }
        tasks = [task for task in block if task.get("name") in names]
        self.assertEqual(len(tasks), len(names))
        tasks[-1]["ansible.builtin.command"]["argv"] = tasks[-1][
            "ansible.builtin.command"
        ]["argv"].replace(
            "playbook_dir ~ '/workaround/manage_overlay.py'", repr(str(manager))
        )
        self.playbook = self.path / "test.yml"
        self.playbook.write_text(
            yaml.safe_dump(
                [
                    {
                        "name": "Test Install workaround tasks",
                        "hosts": "localhost",
                        "gather_facts": False,
                        "vars": {
                            "ao_namespace": "automation-orchestrator",
                            "_kubeconfig_tmp": {"path": "/unused/kubeconfig"},
                        },
                        "tasks": tasks,
                    }
                ],
                sort_keys=False,
            )
        )
        self.env = dict(
            os.environ,
            PATH=str(bindir) + os.pathsep + os.environ["PATH"],
            FAKE_OC_STATE=str(self.state),
            ANSIBLE_NOCOLOR="1",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def run_play(self, *args, succeeds=True):
        result = subprocess.run(
            [
                "ansible-playbook",
                "-i",
                "localhost,",
                "-c",
                "local",
                str(self.playbook),
                *args,
            ],
            env=self.env,
            text=True,
            capture_output=True,
            timeout=90,
        )
        self.assertEqual(
            result.returncode == 0, succeeds, result.stdout + result.stderr
        )
        return result.stdout + result.stderr

    def test_install_reapply_and_remove(self):
        initial = self.state.read_text()
        self.run_play("--check")
        self.assertEqual(initial, self.state.read_text())
        self.run_play()
        self.assertIsNotNone(json.loads(self.state.read_text())["configmap"])
        self.assertIn("changed=0", self.run_play())
        # Removal must still work after the backend image changes on upgrade.
        upgraded = json.loads(self.state.read_text())
        upgraded["deployment"]["spec"]["template"]["spec"]["containers"][0][
            "image"
        ] = "registry.example/backend@sha256:new-release"
        self.state.write_text(json.dumps(upgraded))
        unchanged = self.state.read_text()
        self.run_play("--check", "-e", "ao_workaround_state=absent")
        self.assertEqual(unchanged, self.state.read_text())
        self.run_play("-e", "ao_workaround_state=absent")
        self.assertIsNone(json.loads(self.state.read_text())["configmap"])
        self.assertIn("changed=0", self.run_play("-e", "ao_workaround_state=absent"))

    def test_image_and_source_guards(self):
        data = json.loads(self.state.read_text())
        data["deployment"]["spec"]["template"]["spec"]["containers"][0][
            "image"
        ] = "unknown:latest"
        self.state.write_text(json.dumps(data))
        self.assertIn(
            "Unexpected AO background-worker image", self.run_play(succeeds=False)
        )
        self.assertIsNone(json.loads(self.state.read_text())["configmap"])
        data["deployment"]["spec"]["template"]["spec"]["containers"][0]["image"] = IMAGE
        data["original"] = ORIGINAL + "# unexpected source\n"
        self.state.write_text(json.dumps(data))
        self.assertIn(
            "Unexpected upstream agent source SHA-256", self.run_play(succeeds=False)
        )
        self.assertIsNone(json.loads(self.state.read_text())["configmap"])

    def test_conflicting_configmap_and_invalid_state_fail(self):
        data = json.loads(self.state.read_text())
        data["configmap"] = {"data": {"generic_agent.py": "unexpected"}}
        self.state.write_text(json.dumps(data))
        unchanged = self.state.read_text()
        self.assertIn("unexpected content", self.run_play(succeeds=False))
        self.assertEqual(unchanged, self.state.read_text())
        self.assertIn(
            "Set ao_workaround_state to present or absent",
            self.run_play("-e", "ao_workaround_state=bad", succeeds=False),
        )
        self.assertEqual(unchanged, self.state.read_text())

    def test_removal_rejects_other_deployment_references(self):
        self.run_play()
        data = json.loads(self.state.read_text())
        data["deployment"]["spec"]["template"]["spec"]["volumes"].append(
            {
                "name": "other-user",
                "configMap": {"name": "ao-workshop-structured-output"},
            }
        )
        self.state.write_text(json.dumps(data))
        unchanged = self.state.read_text()
        self.assertIn(
            "other deployment references",
            self.run_play("-e", "ao_workaround_state=absent", succeeds=False),
        )
        self.assertEqual(unchanged, self.state.read_text())


if __name__ == "__main__":
    unittest.main()

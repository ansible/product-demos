"""Exercise install, idempotence, check mode, rollback and version guards."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = "class GenericAgent:\n    async def _execute_structured(self, state, response_schema):\n        return state\n"
BASE_HASH = "e7f21a189bf9863a0a0b1d756cdcb0e28eaa1b2c932168923ca0b6229996344f"
OVERLAY_HASH = "d78d4ab4734d0b9c82a5e7b908722617ed5dfdc13ad1bfb98ff205a20ace4342"
IMAGE = "registry.example/backend@sha256:22279cf11cc61116e4eb5b67d3479d011af668708effe74203913071dcc99f14"


class RolloutTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ao-rollout-test-")
        self.path = Path(self.tmp.name)
        scripts = self.path / "scripts"
        scripts.mkdir()
        for name in (
            "build_overlay.py",
            "manage_overlay.py",
            "structured_method.py.txt",
        ):
            shutil.copy(ROOT / name, scripts / name)
        builder = scripts / "build_overlay.py"
        builder.write_text(
            builder.read_text().replace(
                BASE_HASH, hashlib.sha256(ORIGINAL.encode()).hexdigest()
            )
        )
        original = self.path / "original.py"
        original.write_text(ORIGINAL)
        overlay = self.path / "overlay.py"
        subprocess.run(
            ["python3", str(builder), str(original), str(overlay)],
            check=True,
            capture_output=True,
        )
        manager = scripts / "manage_overlay.py"
        manager.write_text(
            manager.read_text().replace(
                OVERLAY_HASH, hashlib.sha256(overlay.read_bytes()).hexdigest()
            )
        )
        bindir = self.path / "bin"
        bindir.mkdir()
        (bindir / "oc").symlink_to(ROOT / "tests" / "fake_oc.py")
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
        self.inventory = self.path / "inventory.yml"
        self.inventory.write_text(
            "all:\n  children:\n    ao_workshops:\n      hosts:\n        demo:\n          ao_kubeconfig: /unused/test-kubeconfig\n"
        )
        self.env = dict(
            os.environ,
            PATH=str(bindir) + os.pathsep + os.environ["PATH"],
            FAKE_OC_STATE=str(self.state),
            ANSIBLE_NOCOLOR="1",
        )
        self.manager = manager

    def tearDown(self):
        self.tmp.cleanup()

    def run_play(self, *args, succeeds=True):
        cmd = [
            "ansible-playbook",
            "-i",
            str(self.inventory),
            str(ROOT / "rollout.yml"),
            "-e",
            "ao_overlay_script=" + str(self.manager),
            *args,
        ]
        result = subprocess.run(
            cmd, env=self.env, text=True, capture_output=True, timeout=90
        )
        self.assertEqual(
            result.returncode == 0, succeeds, result.stdout + result.stderr
        )
        return result.stdout + result.stderr

    def test_complete_lifecycle_and_image_guard(self):
        initial = self.state.read_text()
        output = self.run_play("--check")
        self.assertIn("would", output)
        self.assertEqual(initial, self.state.read_text())
        output = self.run_play()
        self.assertIn("verified_replicas", output)
        after = json.loads(self.state.read_text())
        self.assertIsNotNone(after["configmap"])
        output = self.run_play()
        self.assertIn("changed=0", output)
        conflict = json.loads(self.state.read_text())
        volumes = conflict["deployment"]["spec"]["template"]["spec"]["volumes"]
        volumes.append(
            {
                "name": "other-user",
                "configMap": {"name": "ao-workshop-structured-output"},
            }
        )
        self.state.write_text(json.dumps(conflict))
        before_conflict = self.state.read_text()
        self.assertIn(
            "other deployment references",
            self.run_play("-e", "ao_workaround_state=absent", succeeds=False),
        )
        self.assertEqual(before_conflict, self.state.read_text())
        volumes.pop()
        self.state.write_text(json.dumps(conflict))
        unchanged = self.state.read_text()
        self.run_play("--check", "-e", "ao_workaround_state=absent")
        self.assertEqual(unchanged, self.state.read_text())
        self.run_play("-e", "ao_workaround_state=absent")
        self.assertIsNone(json.loads(self.state.read_text())["configmap"])
        self.assertIn("changed=0", self.run_play("-e", "ao_workaround_state=absent"))
        data = json.loads(self.state.read_text())
        data["deployment"]["spec"]["template"]["spec"]["containers"][0][
            "image"
        ] = "example/unknown:latest"
        self.state.write_text(json.dumps(data))
        before = self.state.read_text()
        self.assertIn(
            "Unexpected AO background-worker image", self.run_play(succeeds=False)
        )
        self.assertEqual(before, self.state.read_text())

    def test_credential_cleanup_and_conflicting_configmap(self):
        private_tmp = self.path / "private-tmp"
        private_tmp.mkdir()
        self.env["TMPDIR"] = str(private_tmp)
        creds = self.path / "workshop.creds.yml"
        creds.write_text(
            "status:\n  summary:\n    provision_data:\n"
            "      openshift_api_url: https://example.invalid:6443\n"
            "      openshift_api_ca_cert: fake-ca\n"
            "      openshift_cluster_admin_token: sensitive-test-token-12345\n"
        )
        self.inventory.write_text(
            "all:\n  children:\n    ao_workshops:\n      hosts:\n"
            f"        demo:\n          ao_workshop_creds_file: {creds}\n"
        )
        output = self.run_play("--check")
        self.assertNotIn("sensitive-test-token-12345", output)
        self.assertFalse(list(private_tmp.rglob("ao-workshop-kubeconfig-*")))
        data = json.loads(self.state.read_text())
        data["configmap"] = {
            "metadata": {"name": "ao-workshop-structured-output"},
            "data": {"generic_agent.py": "unexpected"},
        }
        self.state.write_text(json.dumps(data))
        before = self.state.read_text()
        self.assertIn("unexpected content", self.run_play(succeeds=False))
        self.assertEqual(before, self.state.read_text())
        self.assertFalse(list(private_tmp.rglob("ao-workshop-kubeconfig-*")))

    def test_source_guard_and_serial_failure(self):
        data = json.loads(self.state.read_text())
        data["original"] = ORIGINAL + "# unexpected image source\n"
        self.state.write_text(json.dumps(data))
        before = self.state.read_text()
        self.assertIn(
            "Unexpected upstream agent source SHA-256",
            self.run_play("--check", succeeds=False),
        )
        self.assertEqual(before, self.state.read_text())
        self.inventory.write_text(
            "all:\n  children:\n    ao_workshops:\n      hosts:\n"
            "        first:\n          ao_kubeconfig: /unused/test-kubeconfig\n"
            "        second:\n          ao_kubeconfig: /unused/test-kubeconfig\n"
        )
        output = self.run_play(succeeds=False)
        self.assertIn("first", output)
        self.assertNotIn("second", output)
        self.assertEqual(before, self.state.read_text())


if __name__ == "__main__":
    unittest.main()

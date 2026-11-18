#!/usr/bin/env python3
"""Manage the workshop-only AO agent overlay using the configured kubeconfig."""

import argparse
import ast
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile

VOLUME = "workshop-structured-output"
CONFIG_MAP = "ao-workshop-structured-output"
TARGET = "/opt/app-root/src/src/syntara/agent_orchestrator/agents/generic_agent.py"
SOURCE_SHA256 = "e7f21a189bf9863a0a0b1d756cdcb0e28eaa1b2c932168923ca0b6229996344f"
IMAGE_DIGEST = "sha256:22279cf11cc61116e4eb5b67d3479d011af668708effe74203913071dcc99f14"
OVERLAY_SHA256 = "d78d4ab4734d0b9c82a5e7b908722617ed5dfdc13ad1bfb98ff205a20ace4342"
METHOD_SHA256 = "b676ca4450420033a6aa323fa729e5ced1a7ea547b5c4d89bd75e999ac98a2d3"


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def kubectl(*args, input_text=None):
    result = subprocess.run(
        ["kubectl", "-n", ARGS.namespace, *args],
        input=input_text,
        text=True,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=210,
    )
    return result.stdout


def get_resource(kind, name):
    raw = kubectl("get", kind, name, "--ignore-not-found", "-o", "json")
    return json.loads(raw) if raw.strip() else None


def get_deployment():
    doc = get_resource("deployment", ARGS.deployment)
    if not doc:
        raise ValueError("Background-worker deployment not found")
    spec = doc["spec"]["template"]["spec"]
    containers = [c for c in spec["containers"] if c["name"] == ARGS.container]
    if len(containers) != 1:
        raise ValueError("Expected exactly one background-worker container")
    return doc, spec, containers[0]


def get_state(doc, spec, container, cm):
    volumes = [v for v in spec.get("volumes", []) if v.get("name") == VOLUME]
    mounts = [
        m
        for m in container.get("volumeMounts", [])
        if m.get("name") == VOLUME or m.get("mountPath") == TARGET
    ]
    if len(volumes) > 1 or len(mounts) > 1:
        raise ValueError("Conflicting overlay volumes or mounts")
    if volumes and volumes[0].get("configMap", {}).get("name") != CONFIG_MAP:
        raise ValueError("Overlay volume is owned by another ConfigMap")
    if mounts and any(
        mounts[0].get(k) != v
        for k, v in {
            "name": VOLUME,
            "mountPath": TARGET,
            "subPath": "generic_agent.py",
            "readOnly": True,
        }.items()
    ):
        raise ValueError("Overlay mount conflicts with the expected mount")
    if bool(volumes) != bool(mounts):
        raise ValueError(
            "Overlay volume and mount are inconsistent; inspect deployment"
        )
    if cm and sha(cm.get("data", {}).get("generic_agent.py", "")) != OVERLAY_SHA256:
        raise ValueError("Existing overlay ConfigMap has unexpected content")
    if mounts and not cm:
        raise ValueError("Overlay is mounted but its ConfigMap is missing")
    return "installed" if mounts else ("orphan_configmap" if cm else "absent")


def patch(doc, patch_ops):
    guarded = [
        {
            "op": "test",
            "path": "/metadata/resourceVersion",
            "value": doc["metadata"]["resourceVersion"],
        }
    ] + patch_ops
    kubectl(
        "patch", "deployment", ARGS.deployment, "--type=json", "-p", json.dumps(guarded)
    )


def rollout_and_verify(doc):
    kubectl("rollout", "status", "deployment/" + ARGS.deployment, "--timeout=180s")
    current, _, _ = get_deployment()
    replicas = current["spec"].get("replicas", 1)
    if replicas < 1:
        raise ValueError("Cannot verify a deployment with zero replicas")
    labels = current["spec"]["selector"].get("matchLabels", {})
    if not labels:
        raise ValueError("Cannot identify worker pods without matchLabels")
    selector = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
    pods = json.loads(kubectl("get", "pods", "-l", selector, "-o", "json"))["items"]
    ready = [
        p
        for p in pods
        if not p["metadata"].get("deletionTimestamp")
        and p.get("status", {}).get("phase") == "Running"
        and any(
            c.get("type") == "Ready" and c.get("status") == "True"
            for c in p["status"].get("conditions", [])
        )
    ]
    if len(ready) != replicas:
        raise ValueError(f"Expected {replicas} ready worker pods, found {len(ready)}")
    for pod in ready:
        output = kubectl(
            "exec",
            "pod/" + pod["metadata"]["name"],
            "-c",
            ARGS.container,
            "--",
            "sha256sum",
            TARGET,
        )
        if output.split()[0] != OVERLAY_SHA256:
            raise ValueError(
                "A ready background worker does not have the expected overlay"
            )
    return len(ready)


def install(doc, spec, container, cm, state):
    if not container["image"].endswith("@" + IMAGE_DIGEST):
        raise ValueError(
            "Unexpected AO background-worker image; review the patch for this version"
        )
    if (
        sha(pathlib.Path(__file__).with_name("structured_method.py.txt").read_text())
        != METHOD_SHA256
    ):
        raise ValueError(
            "Local patch fragment has changed; rebuild and review expected hashes"
        )
    if state == "installed":
        ready = None if ARGS.check else rollout_and_verify(doc)
        return {"changed": False, "state": state, "verified_replicas": ready}
    source = kubectl(
        "exec",
        "deployment/" + ARGS.deployment,
        "-c",
        ARGS.container,
        "--",
        "cat",
        TARGET,
    )
    if sha(source) != SOURCE_SHA256:
        raise ValueError(
            "Unexpected upstream agent source SHA-256; review the patch for this version"
        )
    tree = ast.parse(source)
    cls = next(
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "GenericAgent"
    )
    method = next(
        node
        for node in cls.body
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "_execute_structured"
    )
    lines = source.splitlines(keepends=True)
    original = "".join(lines[method.lineno - 1 : method.end_lineno]).replace(
        "async def _execute_structured(", "async def _execute_structured_native(", 1
    )
    fragment = pathlib.Path(__file__).with_name("structured_method.py.txt").read_text()
    overlay = (
        "".join(lines[: method.lineno - 1])
        + fragment
        + "\n\n"
        + original
        + "".join(lines[method.end_lineno :])
    )
    ast.parse(overlay)
    if sha(overlay) != OVERLAY_SHA256:
        raise ValueError("Generated overlay differs from the validated version")
    if ARGS.check:
        return {"changed": True, "state": state, "would": "install"}
    if not cm:
        with tempfile.TemporaryDirectory(prefix="ao-workaround-") as tmp:
            overlay_path = pathlib.Path(tmp, "generic_agent.py")
            overlay_path.write_text(overlay)
            manifest = kubectl(
                "create",
                "configmap",
                CONFIG_MAP,
                "--from-file=generic_agent.py=" + str(overlay_path),
                "--dry-run=client",
                "-o",
                "json",
            )
            kubectl("create", "-f", "-", input_text=manifest)
    index = spec["containers"].index(container)
    patch(
        doc,
        [
            {
                "op": "test",
                "path": f"/spec/template/spec/containers/{index}/name",
                "value": ARGS.container,
            },
            {
                "op": "add",
                "path": "/spec/template/spec/volumes/-",
                "value": {"name": VOLUME, "configMap": {"name": CONFIG_MAP}},
            },
            {
                "op": "add",
                "path": f"/spec/template/spec/containers/{index}/volumeMounts/-",
                "value": {
                    "name": VOLUME,
                    "mountPath": TARGET,
                    "subPath": "generic_agent.py",
                    "readOnly": True,
                },
            },
        ],
    )
    ready = rollout_and_verify(doc)
    return {"changed": True, "state": "installed", "verified_replicas": ready}


def remove(doc, spec, container, cm, state):
    if state == "absent":
        return {"changed": False, "state": "absent"}
    deployments = json.loads(kubectl("get", "deployments", "-o", "json"))["items"]
    refs = [
        d["metadata"]["name"]
        for d in deployments
        for v in d["spec"]["template"]["spec"].get("volumes", [])
        if v.get("configMap", {}).get("name") == CONFIG_MAP
        and (d["metadata"]["name"] != ARGS.deployment or v.get("name") != VOLUME)
    ]
    if refs:
        raise ValueError(
            "ConfigMap has other deployment references: " + ", ".join(refs)
        )
    if ARGS.check:
        return {"changed": True, "state": state, "would": "remove"}
    if state == "installed":
        index = spec["containers"].index(container)
        mi = next(
            i for i, m in enumerate(container["volumeMounts"]) if m["name"] == VOLUME
        )
        vi = next(i for i, v in enumerate(spec["volumes"]) if v["name"] == VOLUME)
        patch(
            doc,
            [
                {
                    "op": "test",
                    "path": f"/spec/template/spec/containers/{index}/volumeMounts/{mi}/name",
                    "value": VOLUME,
                },
                {
                    "op": "test",
                    "path": f"/spec/template/spec/volumes/{vi}/name",
                    "value": VOLUME,
                },
                {
                    "op": "remove",
                    "path": f"/spec/template/spec/containers/{index}/volumeMounts/{mi}",
                },
                {"op": "remove", "path": f"/spec/template/spec/volumes/{vi}"},
            ],
        )
        kubectl("rollout", "status", "deployment/" + ARGS.deployment, "--timeout=180s")
    kubectl("delete", "configmap", CONFIG_MAP)
    return {"changed": True, "state": "absent"}


def main():
    global ARGS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("install", "remove"))
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--namespace", default="automation-orchestrator")
    parser.add_argument(
        "--deployment", default="automation-orchestrator-background-worker"
    )
    parser.add_argument("--container", default="background-worker")
    ARGS = parser.parse_args()
    doc, spec, container = get_deployment()
    cm = get_resource("configmap", CONFIG_MAP)
    state = get_state(doc, spec, container, cm)
    result = (install if ARGS.action == "install" else remove)(
        doc, spec, container, cm, state
    )
    print(json.dumps(result))


if __name__ == "__main__":
    try:
        main()
    except (
        ValueError,
        subprocess.CalledProcessError,
        subprocess.TimeoutExpired,
        OSError,
    ) as error:
        print(f"Overlay operation failed: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr.strip(), file=sys.stderr)
        sys.exit(1)

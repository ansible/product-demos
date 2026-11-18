#!/usr/bin/env python3
"""Small Kubernetes double for exercising the Ansible rollout without a cluster."""

import copy
import json
import os
import pathlib
import sys

path = pathlib.Path(os.environ["FAKE_OC_STATE"])
s = json.loads(path.read_text())
a = sys.argv[1:]
if a[:1] == ["--context"]:
    a = a[2:]
if a[:1] == ["-n"]:
    a = a[2:]


def save():
    path.write_text(json.dumps(s))


def done(value):
    print(json.dumps(value))
    sys.exit(0)


def fail(message):
    print(message, file=sys.stderr)
    sys.exit(1)


if a[0:2] == ["get", "deployment"]:
    done(s["deployment"])
if a[0:2] == ["get", "deployments"]:
    done({"items": [s["deployment"]]})
if a[0:2] == ["get", "configmap"]:
    if s["configmap"] is not None:
        done(s["configmap"])
    sys.exit(0)
if a[0:2] == ["get", "pods"]:
    done(
        {
            "items": [
                {
                    "metadata": {"name": "worker-1"},
                    "status": {
                        "phase": "Running",
                        "conditions": [{"type": "Ready", "status": "True"}],
                    },
                }
            ]
        }
    )
if a[0] == "exec":
    if "cat" in a:
        print(s["original"], end="")
    elif "sha256sum" in a:
        import hashlib

        print(
            hashlib.sha256(
                s["configmap"]["data"]["generic_agent.py"].encode()
            ).hexdigest(),
            "agent.py",
        )
    else:
        fail("unsupported exec")
    sys.exit(0)
if a[0:2] == ["create", "configmap"]:
    file_arg = next(x for x in a if x.startswith("--from-file="))
    content = pathlib.Path(file_arg.split("=", 2)[2]).read_text()
    done({"metadata": {"name": a[2]}, "data": {"generic_agent.py": content}})
if a[0:3] == ["create", "-f", "-"]:
    if s["configmap"] is not None:
        fail("already exists")
    s["configmap"] = json.load(sys.stdin)
    save()
    sys.exit(0)
if a[0:2] == ["patch", "deployment"]:
    ops = json.loads(a[a.index("-p") + 1])
    deployment = copy.deepcopy(s["deployment"])
    for op in ops:
        bits = op["path"].lstrip("/").split("/")
        node = deployment
        for bit in bits[:-1]:
            node = node[int(bit)] if isinstance(node, list) else node[bit]
        key = bits[-1]
        if op["op"] == "test":
            actual = node[int(key)] if isinstance(node, list) else node[key]
            if actual != op["value"]:
                fail("test failed")
        elif op["op"] == "add":
            if isinstance(node, list) and key == "-":
                node.append(op["value"])
            else:
                node[key] = op["value"]
        elif op["op"] == "remove":
            if isinstance(node, list):
                node.pop(int(key))
            else:
                del node[key]
    s["deployment"] = deployment
    save()
    sys.exit(0)
if a[0:2] == ["rollout", "status"]:
    print("success")
    sys.exit(0)
if a[0:2] == ["delete", "configmap"]:
    s["configmap"] = None
    save()
    sys.exit(0)
fail("unsupported oc arguments: " + repr(a))

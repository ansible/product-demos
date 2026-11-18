# AO structured-output workshop workaround

Some AO Task Agents with an object response schema and no tools report success
with empty output. This opt-in workaround asks the model for JSON text, validates
the result against the schema, and retries up to three times. If no response is
valid, the step fails. Other agent configurations keep their existing behavior.
The metadata for this path reports `workshop_prompt_json`.

This is a temporary workshop overlay, not an operator-supported product fix.
It mounts a patched Python file over the background worker's original file.
The overlay is pinned to one tested image digest and source hash; a different
version fails preflight. Operator reconciliation or an upgrade may remove or
invalidate it. A schema-valid response is not necessarily factually correct.

## Prerequisites

Run from a controller with Python 3, Ansible Core and the OpenShift `oc` CLI.
Use a client compatible with the controller architecture. The controller needs
access to the OpenShift API and permission to read deployments and pods, execute
commands in worker pods, manage ConfigMaps and patch deployments in the AO
namespace. Applying or removing the overlay rolls the worker deployment and can
interrupt running jobs.

Copy [inventory.example.yml](inventory.example.yml) to a secure location. Supply
either a kubeconfig or a Babylon ResourceClaim credentials file for each host;
protect these files and do not commit them. The defaults target the APD
deployment `automation-orchestrator-background-worker`; set
`ao_background_deployment` if the instance uses a different name. Optional
`ao_namespace`, `ao_background_container`, and `ao_context` values can also be
set per host. Context applies only to a kubeconfig.

## Apply and verify

Start with one instance during a maintenance window, then run isolated Task
Agent tests using that instance's model and schema before continuing. Check mode
performs a read-only preflight against OpenShift. It does not verify pod hashes
when the overlay is already installed.

```sh
ansible-playbook -i /secure/path/inventory.yml infrastructure/ao/workaround/rollout.yml --limit workshop_01 --check
ansible-playbook -i /secure/path/inventory.yml infrastructure/ao/workaround/rollout.yml --limit workshop_01
ansible-playbook -i /secure/path/inventory.yml infrastructure/ao/workaround/rollout.yml --limit workshop_01
```

The normal run waits for the rollout and verifies the overlay hash on every
ready worker. Repeated runs verify the installed overlay without changing it.
After validating the canary, remove `--limit` to apply sequentially to the rest
of the inventory. The playbook stops on the first failure. It does not run AO
inference tests or downstream AAP jobs. Verify those separately, and recheck the
deployment after operator changes.

## Rollback

```sh
ansible-playbook -i /secure/path/inventory.yml infrastructure/ao/workaround/rollout.yml --limit workshop_01 -e ao_workaround_state=absent --check
ansible-playbook -i /secure/path/inventory.yml infrastructure/ao/workaround/rollout.yml --limit workshop_01 -e ao_workaround_state=absent
```

Rollback restores the image file and deletes the ConfigMap after the worker
rollout. Unexpected contents, conflicting mounts, and other deployment
references stop the operation for inspection.

Run the local rollout tests from the repository root with:

```sh
python3 -m unittest discover -s infrastructure/ao/workaround/tests -v
```

These tests use a simulated `oc` client and do not replace a live canary.

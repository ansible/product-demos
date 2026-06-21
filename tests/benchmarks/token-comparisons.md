# Token Authentication Performance Comparison

## Background

The `infra.aap_configuration.dispatch` role configures AAP resources (projects,
templates, credentials, workflows, etc.) by calling `ansible.controller` modules
for each resource. When password-based authentication is used, every single
module invocation goes through this cycle:

1. **POST** `/api/controller/v2/tokens/` with basic auth to create an OAuth token
2. Use that token for the actual API work (GET, POST, PATCH)
3. **DELETE** `/api/controller/v2/tokens/<id>/` to revoke the token on exit

This means each module call pays 2 extra API round-trips just for auth. With
dozens of resources spread across many resource types (credentials, projects,
inventory sources, templates, workflows, notifications, etc.), this overhead
compounds.

The `ansible.platform.token` module lets us create a single OAuth token
up-front and pass it to the dispatch role via `controller_oauthtoken`. When
a pre-created token is present, the `ansible.controller` modules skip the
`authenticate()` and `logout()` calls entirely, reusing the one token for every
API request.

### What we're comparing

- **`setup_demo.yml`** (token): Creates a token via `ansible.platform.token`,
  passes it to dispatch, then revokes it in an `always` block.
- **`wo_token_setup.yml`** (no-token): Original playbook that relies on
  password env vars. Each module creates and destroys its own token internally.

Both playbooks configure the same set of Linux demo resources. Between each run,
`utils/teardown_demo.yml` removes all created resources to ensure a clean slate.

## Initial results (invalidated)

Early testing only tore down and re-created **job templates**, which meant
dispatch was only calling `ansible.controller` for a single resource type. The
results showed no meaningful difference:

token (setup_demo.yml)

| run | total time |
|-----|------------|
| #1  | 2:08.85    |
| #2  | 2:23.02    |
| #3  | 2:06.18    |

no-token (wo_token_setup.yml)

| run | total time |
|-----|------------|
| #1  | 2:18.03    |
| #2  | 2:26.21    |
| #3  | 2:23.24    |

The savings were negligible because with only one resource type in play, the
token create/delete overhead was a tiny fraction of the total runtime.

After examining the `ansible.controller` module source
(`ControllerAPIModule.authenticate()`), we confirmed that password auth creates a
token per module invocation. The benefit scales with the **number of resource
types and items** being configured -- the more module calls, the more round-trips
saved.

## Full-stack results

After building a proper teardown playbook that removes all resource types
(workflows, templates, notifications, inventory sources, groups, projects,
credentials, credential types, execution environments, organizations, and
gateway resources), we re-ran benchmarks using the complete Linux demo
configuration.

token (setup_demo.yml)

| run | total time |
|-----|------------|
| #1  | 2:33.62    |
| #2  | 2:32.83    |
| #3  | 2:28.17    |
| #4  | 2:18.58    |
| avg | **2:28.30**|

no-token (wo_token_setup.yml)

| run | total time |
|-----|------------|
| #1  | 2:52.67    |
| #2  | 2:42.66    |
| #3  | 2:43.69    |
| #4  | 2:43.46    |
| avg | **2:45.62**|

### Observations

- Token auth is consistently faster across all runs, averaging ~2:28 vs ~2:45
  (roughly **10-12% improvement**).
- The no-token runs are very stable (~2:43) while token runs show more variance,
  likely due to external factors (API server load, network jitter).
- The gap should widen further when configuring multiple demo categories
  (linux + windows + cloud + network) since more resource types means more
  module invocations and more skipped auth round-trips.

### Bug found along the way

During testing we discovered a bug in the `ansible.platform.token` module
(`aap_module.py`). When passing a registered variable as `existing_token` for
deletion, the module failed with `"Unable to process delete of item due to
missing data 'url'"`. The token data was nested inside
`ansible_facts.aap_token` but the module expected it at the top level. A fix
was applied to `token.py` to unwrap the registered result when the `url` key
is not found at the top level.

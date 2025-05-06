# GitHub Actions
## Background
We want to make attempts to run our integration tests in the same manner wether using GitHub actions or on a developers's machine locally. For this reason, the tests are curated to run using conatiner images. As of this writing, two images exist which we would like to test against:
  - quay.io/ansible-product-demos/apd-ee-24:latest
  - quay.io/ansible-product-demos/apd-ee-25:latest

These images are built given the structure defined in their respective EE [definitions][../execution_environments]. Because they differ (mainly due to their python versions), each gets some special handling.

## Troubleshooting GitHub Actions

### Interactive
It is likely the most straight-forward approach to interactively debug issues. The following podman command tries to replicate what our GitHub action is configured to do:
```
podman run \
           --user root  \
           -v $(pwd):/runner:Z \
           -it \
           <image>
           /bin/bash
```

where `<image>` is one of `quay.io/ansible-product-demos/apd-ee-25:latest`, `quay.io/ansible-product-demos/apd-ee-24:latest`  

For the 24 EE, the python interpreriter verions is set for our pre-commit script like so: `USE_PYTHON=python3.9 ./.github/workflows/run-pc.sh`
The 25 EE is similary run but without the need for this variable: `./.github/workflows/run-pc.sh`

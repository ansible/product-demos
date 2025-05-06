# GitHub Actions
## Troubleshooting

### Dupliting errors
```
podman run \
           --user root  \
           -v $(pwd):/runner:Z \
           -it \
           <image> \
           ./.github/workflows/run-pc.sh
```
where `<image>` is one of `quay.io/ansible-product-demos/apd-ee-25:latest`, `quay.io/ansible-product-demos/apd-ee-24:latest`  

This essentially runs one of the two github actions we have. Ideally it shows the same error that occurs in CI.

### Interactive
```
podman run \
           --user root  \
           -v $(pwd):/runner:Z \
           -it \
           <image>
           /bin/bash
```

where `<image>` is one of `quay.io/ansible-product-demos/apd-ee-25:latest`, `quay.io/ansible-product-demos/apd-ee-24:latest`  

This is an interactive verison.

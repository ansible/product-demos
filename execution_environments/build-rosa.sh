#!/bin/bash
# Build script for the ROSA lifecycle Execution Environment image.
# Usage: ./build-rosa.sh [manifest_name]
#   default manifest: quay.io/acme_corp/rosa-ee

manifest=${1:-quay.io/acme_corp/rosa-ee}
image="${manifest##*/}"

if [[ "$(uname -s)" == "Linux" ]]; then
    source /etc/os-release
    if [[ "$ID" == "rhel" ]]; then
        echo "RHEL does not include the necessary QEMU RPMs for creating multi-arch EE images,"
        echo "please run this script on a Fedora system with the qemu-user-static RPM installed"
        exit 1
    fi
    if [[ "$ID" == "fedora" ]]; then
        if ! rpm -q --quiet qemu-user-static; then
            echo "Please install the qemu-user-static RPM before continuing"
            exit 1
        fi
    fi
fi

if [[ -z $ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN || -z $ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN ]]; then
    echo "A valid Automation Hub token is required, set the following environment variables before continuing:"
    echo "export ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN=<token>"
    echo "export ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN=<token>"
    exit 1
fi

if ! podman login --get-login registry.redhat.io > /dev/null; then
    echo "Run 'podman login registry.redhat.io' before continuing"
    exit 1
fi

# create EE definition
rm -rf ./context/*
ansible-builder create \
    --file rosa-ee.yml \
    --context ./context \
    -v 3 | tee ansible-builder-rosa.log

_tag=$(date +%Y%m%d)
podman manifest rm ${manifest}:${_tag} 2>/dev/null

podman manifest create ${manifest}:${_tag}

for arch in amd64 arm64; do
    _baseurl=https://mirror.openshift.com/pub/openshift-v4/${arch}/dependencies/rpms/4.18-el9-beta/
    _rpm=$(curl -s ${_baseurl} | grep openshift-clients-4 | grep href | cut -d\" -f2)

    pushd ./context/ > /dev/null
    podman build --platform linux/${arch} \
      --build-arg ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN \
      --build-arg ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN \
      --build-arg OPENSHIFT_CLIENT_RPM="${_baseurl}${_rpm}" \
      --manifest ${manifest}:${_tag} . \
      | tee podman-build-rosa-${arch}.log
    popd > /dev/null
done

echo ""
echo "Build complete. To push:"
echo "  podman tag ${manifest}:${_tag} ${manifest}:latest"
echo "  podman manifest push --all ${manifest}:${_tag}"
echo "  podman manifest push --all ${manifest}:latest"

#!/bin/bash
manifest=${1:-quay.io/ansible-product-demos/apd-ee-26}
image="${manifest##*/}"  # everything up to and including last slash, e.g. "apd-ee-26"

if [[ "$(uname -s)" == "Linux" ]]
then
    source /etc/os-release

    if [[ "$ID" == "rhel" ]]
    then
        echo "RHEL does not include the necessary QEMU RPMs for creating multi-arch EE images,"
        echo "please run this script on a Fedora system with the qemu-user-static RPM installed"
        exit 1
    fi

    if [[ "$ID" == "fedora" ]]
    then
        if ! rpm -q --quiet qemu-user-static
        then
            echo "Please install the qemu-user-static RPM before continuing, it is required"
            echo "for building multi-arch EE images"
            exit 1
        fi
    fi
fi

if [[ -z $ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN || -z $ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN ]]
then
    echo "A valid Automation Hub token is required, set the following environment variables before continuing:"
    echo "export ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN=<token>"
    echo "export ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN=<token>"
    exit 1
fi

# log in to pull the base EE image
if ! podman login --get-login registry.redhat.io > /dev/null
then
    echo "Run 'podman login registry.redhat.io' before continuing"
    exit 1
fi

# create EE definition
rm -rf ./context/*
ansible-builder create \
    --file ${image}.yml \
    --context ./context \
    -v 3 | tee ansible-builder.log

# remove existing manifest if present
_tag=$(date +%Y%m%d)
podman manifest rm ${manifest}:${_tag}

# create manifest for EE image
podman manifest create ${manifest}:${_tag}

# for the openshift-clients RPM, microdnf doesn't support URL-based installs
# and HTTP doesn't support file globs for GETs, use multiple steps to determine
# the correct RPM URL for each machine architecture
for arch in amd64 arm64
do
    _baseurl=https://mirror.openshift.com/pub/openshift-v4/${arch}/dependencies/rpms/4.18-el9-beta/
    _rpm=$(curl -s ${_baseurl} | grep openshift-clients-4 | grep href | cut -d\" -f2)

    # build EE for multiple architectures from the EE context
    pushd ./context/ > /dev/null
    podman build --platform linux/${arch} \
      --build-arg ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN \
      --build-arg ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN \
      --build-arg OPENSHIFT_CLIENT_RPM="${_baseurl}${_rpm}" \
      --manifest ${manifest}:${_tag} . \
      | tee podman-build-${arch}.log
    popd > /dev/null
done

# inspect manifest content
#podman manifest inspect ${manifest}:${_tag}

# tag manifest as latest
#podman tag ${manifest}:${_tag} ${manifest}:latest

# push all manifest content to repository
# using --all is important here, it pushes all content and not
# just the native platform content
#podman manifest push --all ${manifest}:${_tag}
#podman manifest push --all ${manifest}:latest

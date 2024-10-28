#!/bin/bash

# array of images to build
ee_images=(
    "apd-ee-24"
    "apd-ee-25"
)

for ee in "${ee_images[@]}"
do
    echo "Building EE image ${ee}"

    # build EE image
    ansible-builder build \
        --file ${ee}.yml \
        --context ./ee_contexts/${ee} \
        --build-arg ANSIBLE_GALAXY_SERVER_CERTIFIED_TOKEN \
        --build-arg ANSIBLE_GALAXY_SERVER_VALIDATED_TOKEN \
        -v 3 \
        -t quay.io/ansible-product-demos/${ee}:$(date +%Y%m%d)

    if [[ $? == 0 ]]
    then
        # tag EE image as latest
        podman tag \
            quay.io/ansible-product-demos/${ee}:$(date +%Y%m%d) \
            quay.io/ansible-product-demos/${ee}:latest
    fi
done

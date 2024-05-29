Role Name
=========

This Ansible role helps configure Operators on the Openshift Cluster to support VM migrations. Tasks include
- Configure Catalog Sources to use mirroring repository for Operators
- Create and configure Operators


Requirements
------------

Any pre-requisites that may not be covered by Ansible itself or the role should be mentioned here. For instance, if the role uses the EC2 module, it may be a good idea to mention in this section that the boto package is required.

Role Variables
--------------

The task `operators/catalog_sources.yml` needs following variables:

- **Variable Name**: `cluster_config_catalog_sources`
  - **Type**: List
  - **Description**: A list of custom CatalogSources configurations used as loop variables to generate Kubernetes manifest files from the  template `catalog_source.j2` for CatalogSource. If the variable is not available, no manifest is created.
  - **Example**:
    ```yaml
    cluster_config_catalog_sources:
      - name: redhat-marketplace2
        source_type: grpc
        display_name: Mirror to Red Hat Marketplace
        image_path: internal-registry.example.com/operator:v1
        priority: '-300'
        icon:
          base64data: ''
          mediatype: ''
        publisher: redhat
        address: ''
        grpc_pod_config: |
          nodeSelector:
            kubernetes.io/os: linux
            node-role.kubernetes.io/master: ''
          priorityClassName: system-cluster-critical
          securityContextConfig: restricted
          tolerations:
            - effect: NoSchedule
              key: node-role.kubernetes.io/master
              operator: Exists
            - effect: NoExecute
              key: node.kubernetes.io/unreachable
              operator: Exists
              tolerationSeconds: 120
            - effect: NoExecute
              key: node.kubernetes.io/not-ready
              operator: Exists
              tolerationSeconds: 120
        registry_poll_interval: 10m
    ```

The task `operators/operator_config.yaml` needs following variables:

- **Variable Name**: `cluster_config_operators`
  - **Type**: List
  - **Description**: A list of operators to be installed on OCP cluster
- **Variable Name**: `cluster_config_[OPERATOR_NAME]`
  - **Type**: Dict
  - **Description**: Configuration specific to each operator listed in `cluster_config_operators`. Includes settings for namespace, operator group, subscription, and any extra resources
  - **Example**: Assume the `cluster_config_operators` specifies these operators:
  ```yaml
  cluster_config_operators:
    - cnv
    - oadp
  ```
  then the corresponding `cluster_config_mtv` and `cluster_config_cnv` can be configured as following:
  ```yaml
  cluster_config_cnv_namespace: openshift-cnv
  cluster_config_cnv:
  namespace:
    name: "{{ cluster_config_cnv_namespace }}"
  operator_group:
    name: kubevirt-hyperconverged-group
    target_namespaces:
      - "{{ cluster_config_cnv_namespace }}"
  subscription:
    name: kubevirt-hyperconverged
    starting_csv: kubevirt-hyperconverged-operator.v4.13.8
  extra_resources:
    - apiVersion: hco.kubevirt.io/v1beta1
      kind: HyperConverged
      metadata:
        name: kubevirt-hyperconverged
        namespace: "{{ cluster_config_cnv_namespace }}"
      spec:
        BareMetalPlatform: true

  cluster_config_oadp_namespace: openshift-adp
  cluster_config_oadp:
  namespace:
    name: "{{ cluster_config_oadp_namespace }}"
  operator_group:
    name: redhat-oadp-operator-group
    target_namespaces:
      - "{{ cluster_config_oadp_namespace }}"
  subscription:
    name: redhat-oadp-operator-subscription
    spec_name: redhat-oadp-operator
  ```
Dependencies
------------

A list of other roles hosted on Galaxy should go here, plus any details in regards to parameters that may need to be set for other roles, or variables that are used from other roles.

Example Playbook
----------------

An example of configuring a CatalogSource resource:
```
- name: Configure Catalog Sources for Operators
  hosts: localhost
  gather_facts: false
  tasks:
    - ansible.builtin.include_role:
        name: cluster_config
        tasks_from: operators/catalog_sources
```

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).

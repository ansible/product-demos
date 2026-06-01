# OpenShift Demos

## Table of Contents
- [OpenShift Demos](#openshift-demos)
  - [Table of Contents](#table-of-contents)
  - [About These Demos](#about-these-demos)
    - [Jobs](#jobs)
  - [Suggested Usage](#suggested-usage)

## About These Demos
This category of demos shows examples of OpenShift operations and management with Ansible Automation Platform. The list of demos can be found below. See the [Suggested Usage](#suggested-usage) section of this document for recommendations on how to best use these demos.

### Jobs
- [**OpenShift / Dev Spaces**](devspaces.yml) - Install and deploy dev spaces on OCP cluster. After this job has run successfully, login to your OCP cluster, click the application icon (to the left of the bell icon in the top right) to access Dev Spaces
- [**OpenShift / GitLab**](gitlab.yml) - Install and deploy GitLab on OCP.
- [**OpenShift / EDA / Install Controller**](eda/install.yml) - Install and deploy EDA Controller instance using the AAP OpenShift operator.
- [**OpenShift / CNV / Install Operator**](cnv/install.yml) - Install the Container Native Virtualization (CNV) operator and all its required dependencies.
- **OpenShift / CNV / Infra Stack** - Workflow Job Template to build out infrastructure necessary to run jobs against VMs in OpenShift Virtualization.
    - [**OpenShift / CNV / Create RHEL VM**](cnv/install.yml) - Install the Container Native Virtualization (CNV) operator and all its required dependencies.
- **OpenShift / CNV / Patch CNV Workflow** - Workflow Job Template to snapshot and patch VMs deployed in OpenShift Virtualization.
    - [**OpenShift / CNV / Create VM Snapshots**](cnv/snapshot.yml) - Create snapshot of VMs running in CNV.
    - [**OpenShift / CNV / Patch**](cnv/patch.yml) - Patch VMs in OpenShift CNV, when run in `run` mode build out container native patching report and display link to the user.
    - [**OpenShift / CNV / Restore Latest VM Snapshots**](cnv/snapshot.yml) - Restore VM in CNV to last snapshot.
- [**OpenShift / CNV / Delete VM**](cnv/install.yml) - Deletes VMs in OpenShift CNV.

**Hosted control planes (HyperShift on KubeVirt)** — deploy and tear down a hosted OpenShift cluster whose workers run as KubeVirt VMs on the management cluster. Requires OpenShift Virtualization (CNV), multicluster engine (MCE), and a management cluster that meets [HyperShift KubeVirt prerequisites](https://hypershift.pages.dev/how-to/kubevirt/create-kubevirt-cluster/) (for example wildcard Routes, default `StorageClass`, `LoadBalancer` support such as MetalLB, and enough worker capacity).

- [**OpenShift / HCP / Install Operator**](hcp/install_operator.yml) — Install the multicluster engine operator and create the `MultiClusterEngine` custom resource (HyperShift components enabled). Uses the shared `demo.openshift.cluster_config` role; channel is defined in `cluster_config` defaults.
- [**OpenShift / HCP / Management prerequisites**](hcp/management_prereqs.yml) — Patch the default `IngressController` so wildcard DNS routes are allowed (`routeAdmission.wildcardPolicy: WildcardsAllowed`). Run once per management cluster before deploy (or confirm the setting already exists).
- [**OpenShift / HCP / Deploy**](hcp/deploy.yml) — Create a `HostedCluster` and `NodePool` on the KubeVirt platform (manifests rendered from [`hcp/templates/hostedcluster.yml.j2`](hcp/templates/hostedcluster.yml.j2) and [`hcp/templates/nodepool.yml.j2`](hcp/templates/nodepool.yml.j2)). Job survey sets cluster name, worker count, release image, SSH key, optional etcd `StorageClass`, optional APIServer Route hostname, and related options.
- [**OpenShift / HCP / Delete**](hcp/delete.yml) — Remove the `NodePool`(s) and `HostedCluster`. Survey can enable finalizer stripping and optional deletion of the `clusters-<name>` control-plane namespace for stuck or partial installs.

## Pre Setup
These demos require an OpenShift cluster to deploy to. Luckily the default Ansible Product Demos item from [demo.redhat.com](https://demo.redhat.com) includes an OpenShift cluster. Most of the jobs require an `OpenShift or Kubernetes API Bearer Token` credential in order to interact with OpenShift. When ordered from RHDP this credential is configured for the user.

## Suggested Usage
**OpenShift / EDA / Install Controller** - This job uses the `admin` Controller user's password to configure the EDA controller login of the same name. This job displays the created route after finished and takes roughly 2.5 minutes to run.

**OpenShift / CNV /  Deploy Automation Hub and sync EEs and Collections** - A custom credential type is created for the use in this WJT, `Usable Hub Credential` and it must be filled out in order to pull content from console.redhat.com. This workflow takes roughly 30 minutes to run. This workflow includes the following Job Templates:
- **OpenShift / Hub / Install Automation Hub** - This job does not require a hub credential

- **OpenShift / Hub / Sync EE Registries** - The registries can be configured via `extra_vars` and conforms roughly to those described in [infra.ah_configuration.ah_ee_registry](https://console.redhat.com/ansible/automation-hub/repo/validated/infra/ah_configuration/content/module/ah_ee_registry/).

- **OpenShift / Hub / Sync Collection Repositories** - The collections can be configured via `extra_vars` and conforms roughly to those described in [infra.ah_configuration.collection_repository_sync](https://console.redhat.com/ansible/automation-hub/repo/validated/infra/ah_configuration/content/role/collection_repository_sync/).

**OpenShift / CNV / Install Operator** - This job takes no parameters, to ensure the CNV operator is fully operational it provisions a VM in CNV which is cleaned up upon success.

**OpenShift / CNV / Infra Stack** - This workflow takes three parameters, SSH public key, RHEL activation key, and org ID. The SSH public key is placed as an SSH authorized key, thus in order to then authenticate to these VMs the `Machine Credential` `Demo Credential` must be configured with the private key pair associated with the SSH public key. The RHEL activation key and ID are to receive updates from the DNF repositories for the final patching job. This workflow includes the following Job Templates:
- **OpenShift / CNV / Create RHEL VM** - creates a VM using OpenShift Virtualization
**OpenShift / CNV / Patch CNV Workflow** - This workflow takes an ansible host string as a parameter, by default the hosts generated by APD in CNV are of the format `<namespace>-<vm name>`, for example `openshift-cnv-rhel9`. This workflow includes the following Job Templates:

- **OpenShift / CNV / Create VM Snapshots** - Creates snapshots of VMs relevant to the workflow
- **OpenShift / CNV / Patch** - Patches relevant VMs and generate patching report
- **OpenShift / CNV / Restore Latest VM Snapshots** - restores VMs to their latest snapshot, for the workflow this is invoked upon failure of the patching job. The same host string is used by this job template as the others in the workflow.

**OpenShift / CNV / Delete VM** - Delete VMs based on host string pattern, similar to the other CNV jobs.

**OpenShift / HCP** — Run jobs in order: **CNV / Install Operator** (KubeVirt) → **HCP / Install Operator** (MCE) → **HCP / Management prerequisites** (wildcard routes) → **HCP / Deploy**. Use the **OpenShift** API token credential. Surveys drive cluster name, namespace (default `clusters`), OCP release image, worker replicas, SSH public key for nodes, and optional settings (etcd PVC size/class, CAPK image override, APIServer Route FQDN — if left blank, deploy publishes the API via `LoadBalancer`, which requires a working `LoadBalancer` provider on the management cluster). **HCP / Delete** removes the hosted cluster; enable finalizer stripping only for resources stuck in `Terminating`.

For troubleshooting provisioning (infrastructure not ready, etcd not created yet, APIServer Route hostname errors, or `LoadBalancer` Services pending), see the comment header in [`hcp/deploy.yml`](hcp/deploy.yml) and your MCE/HyperShift support matrix for the chosen release image.

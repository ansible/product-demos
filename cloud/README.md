# Ansible Cloud Demos

## Setup
   > These steps may differ if you in your environment

### Add AWS Credentials

1) Add AWS Access and Secret key to the AWS Credential created by the setup job

### Add Workshop Credential Password

1) Add the password used to login to Controller. This allows you to connect to Windows Servers provisioned with Create VM job. Required until [RFE](https://github.com/ansible/workshops/issues/1597]) is complete

### Remove Inventory Variables

1) Remove Workshop Inventory variables on the Details page of the inventory. Required until [RFE](https://github.com/ansible/workshops/issues/1597]) is complete

### Getting your Puiblic Key for Create Infra Job

1) Connect to the command line of your Controller server. This is easiest to do by opening the VS Code Web Editor from the landing page where you found the Controller login details.
2) Open a Terminal Window in the VS Code Web Editor.
3) SSH to one of your linux nodes (eg. `ssh node1`). This should log you into the node as `ec2-user`
4) `cat .ssh/authorized_keys` and copy the key listed including the  `ssh-rsa` prefix


## Demos

### Cloud / Create Infra

The Create Infra job builds cloud infrastructure based on the provider definition in the included `demo.cloud` collection.

### Cloud / Create VM

The Create VM job builds a VM in the given provider based on the included `demo.cloud` collection. VM blueprints define variables for each provider that override the collection roles.
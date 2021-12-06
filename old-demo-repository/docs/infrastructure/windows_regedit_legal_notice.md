# Demo: Windows Use Regedit to update legal notice

[Click here to return to master demo list](../../README.md#demo-repository)

## Table of Contents

- [Demo: Windows Use Regedit to update legal notice](#demo-windows-use-regedit-to-update-legal-notice)
  - [Table of Contents](#table-of-contents)
  - [Objective](#objective)
  - [What business problem is solved?](#what-business-problem-is-solved)
  - [Features show cased](#features-show-cased)
  - [Video](#video)
  - [Guide](#guide)

## Objective

Demostrate how anisble can be used to automate the updating of Windows registry items such as the legal notice enterprise wide witth one simple playbook.

## What business problem is solved?

- **speed to production**:
reducing human time to make large scale changes across an enterprise
- **reduce human error**:
automation of routine manual processes
- **reduce complexity**:
does not require a System Administrator to be familar with Ansible or even regedit. Provides a self services option to make technical changes to 1000's of devices
  
## Features show cased

- Push button deployment
- Self Service IT - Surveys

For description of these and other features of the Red Hat Ansible Automation Platform please refer to the [features README](../features.md)

## Video

[Windows Regedit Legal Notice Video Demo](https://www.youtube.com/watch?v=L_S74rdLat8&list=PLdu06OJoEf2bnEaWYY0DXF90KkyqjVqOF&index=2)

## Guide

1. Login to Ansible Platform UX

2. Navigate to **Templates**

     ![job templates](../images/templates.png)

3. Click the rocket next to **INFRASTRUCTURE / Windows regedit legal notice** to launch the Job

     ![rocket launch](../images/rocket.png)

4. The survey will prompt you for the title and text of the legal notice.

     ![survey choice](../images/windows_regedit_legal_notice/windows_regedit_legal_survey.jpeg)

5. Type in the Tile and Text and press **NEXT**

     ![survey preview](../images/windows_regedit_legal_notice/windows_regedit_legal_survey_preview.jpeg)

     Explain to audience what is happening here depending on audience persona

    **Persona A**: Technical audience that has written Ansible Playbooks before:
    Surveys create variables that the Job can use within Ansible Playbooks. This gives you the ability to create one playbook that can be used for any future updates. In this case you can update the title and test of the legal notice. Again saving you time and effort to modify the playbook directly each time you need to make an update.  In the screenshot you will see the variables are named **text_legal_notice** and **title_legal_notice**  with some default values but the admin can modify them as they need.

    **Persona B**: Decision maker audience, IT manager or above:
    reiterate business values above.  This allows a non subject matter expert the ability to automate routine tasks within a Windows environment.  They can make these changes on all windows devices with one run. Freeing them from the mundance and repeative task for application installation while maintaining the highest level of security and compliance across your organization. They can do all this with little to no risk as no chance of a fat-finger mistake which in regedit can be disasterous. In the event that your IT process does not allow the Red Hat Ansible Automation Platform to be the front end, it has a rich and powerful API that can work with existing workflows such as ServiceNow.

6. Execute the job by pressing the green **LAUNCH** button

7. Explain what is happening:

     - Job has started executed in the background.  The user can navigate off this page and the job will continue to execute.
     - On the left is the **Job Details Pane** labeled simply with **DETAILS**.  This information is logged and tells you who, what, when and how.
       - **who** - who launched the job, in this example is the admin user
       - **what** - the project and Ansible Playbook used, and which credential to login to the infrastructure
       - **when** - time stamps for start, end and duration of the job run.
       - **how** - the job status (pass, fail), enviornment and execution node
     - The larger window on the right is the **Standard Out Pane**.  This provides the same console output the user would be used to on the command-line for troubleshooting purposes.  Some important takeways to showcase are:
       - aggregate info is at the top including the amount of Plays, tasks, hosts and time duration.
       - this pane can be expanded to take up entire browser window
       - Ansible Playbook can be downloaded for troubleshooting purposes
       - **click on task output** to show them task-by-task JSON output that can be used for troubleshooting or just getting additional information
       ![task breakdown](../images/windows_regedit_legal_notice/windows_regedit_legal_task_output.jpeg)

8. Circle back and summarize

     You need to circle back what has been showcased to the [business reasons listed above](#what-business-problem-is-solved).  You are welcome to verify on the Windows hosts that legal notice was actually changed but unless you have a very technical audience you are going to start losing folks.  The real business solution here is automating away the mundane and repetative.

9. Show new legal notice (optional)

     Using some version of RDP you will need to connect to the windows host. The info needed to connect can be found within "inventories" You will need to navigate to Inventories first. Then click on "workshop inventory". Then click on "hosts". You should see your list of hosts. Click on your windows host which will give you the host IP, the username and the password required to connect via RDP.

     ![Inventory Hosts](../images/windows_regedit_legal_notice/windows_regedit_legal_host_info.jpg)

     Once you connect you will see both the title and text first thing. It should match what you updated it to.

---
You have finished this demo.  [Click here to return to master demo list](../../README.md#demo-repository)

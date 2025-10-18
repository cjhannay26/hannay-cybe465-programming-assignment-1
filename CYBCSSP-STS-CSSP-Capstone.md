## 🧪 STS-CSSP-Capstone Testing Strategy

This document defines the goal of writing tests, what tests will be written, and when tests will be written, as well as the testing environment and procedures.

---

### **Goal of Writing Tests**

The goal of writing tests is to ensure that the application is working the way it is intended to. This is to catch any issues early in the development process and before deploying any changes to production.

* **Test Type:** **Feature tests** are the main tests that will be written, which verify user interaction is functioning properly.
* **Basis:** These tests will be written according to software requirements and design documentation.
* **Schedule:** Tests will be written **asynchronously**, preferably before development takes place but also retroactively if need be.

---

### **Testing Environment**

This section defines how to set up an environment to run tests.

1.  **Git**
    * Installation command: `sudo apt install git`
2.  **Docker Engine**
    * Installation commands:
        ```bash
        curl -fsSL [https://get.docker.com-o](https://get.docker.com-o) get-docker.sh
        sudo sh get-docker.sh
        ```
    * **Note:** `Curl` is required if you use the code above to install Docker Engine. You can install it using the command `sudo apt install curl`.

---

### **Testing Procedure**

This defines how tests will be run.

#### **Local Testing**
1.  Clone the repository.
2.  Checkout the main branch.
3.  Cd to the project root directory.
4.  Start the rails server (e.g., `rails server`).
5.  Run tests:
    * Run all tests: (e.g., `rspec`)
    * Run **free** tests: (e.g., `rspec spec/features/free`)
    * Run **not free** tests: (e.g., `rspec spec/features/not_free`)

#### **Docker Testing**
1.  Clone the repository.
2.  Checkout the main branch.
3.  Build the Docker testing container (e.g., `docker build -t "cssp_test".`).
    * *The example above assumes the Dockerfile is named Dockerfile and the path is the project directory*.
    * *It also assumes the user has been added to the Docker group*. If not, you can prepend Docker commands with `sudo`.
4.  Run the Docker testing container (e.g., `docker run -t "cssp_test"`).
    * The `ENTRYPOINT` to the Docker container automatically runs all tests. The results of running all the tests will then be displayed in the terminal.

---

### **Testing Schedule**

This defines when and what tests will be run.

* All tests will be run when a **commit is made** to the repository, helping developers to quickly see if their code changes break anything.
* All tests will also be run when a **pull request is made**, ensuring good code quality on the main branch.
* If tests fail on a pull request, a follow-up commit can be made to fix any issues.
* Once all tests pass, the pull request will automatically be merged into the main branch.

---

### **Test List**

A list of all current tests.

#### **Free Tests**

A list of all tests that **do not cost money** to run (i.e., tests don't make calls to the AWS API).

| Name | Purpose | Status | File Path | Notes | Use Case IDS |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Sign up | checks if a user to sign up | **Pass** | railsapp/cssp/spec/features/free/sign_up_user.rb | None | 1 |
| Log in | checks if a user to log in | **Pass** | railsapp/cssp/spec/features/free/log_in_spec.rb | None | 2 |
| Log out | checks if the user can log out | **Pass** | railsapp/cssp/spec/features/free/log_out_spec.rb | None | 8 |
| Create group | checks if a group can be created | **Pass** | railsapp/cssp/spec/features/free/create_group_spec.rb | None | 17 |
| Delete group | checks if a group can be deleted | **Fail** | railsapp/cssp/spec/features/free/delete_group_spec.rb | Test failure; Trouble dealing with turbo confirm | 19 |
| Add user | checks if a user can be added to the database | **Fail** | railsapp/cssp/spec/features/free/add_user_spec.rb | UI failure | 13 |
| Add user to group | checks if a user can be added to a group | **Pass** | railsapp/cssp/spec/features/free/add_user_to_group_spec.rb | None | 20 |
| Create secret | checks if a secret can be made with specified information | **Pass** | railsapp/cssp/spec/features/free/create_secret_spec.rb | None | 55 |
| Delete secret | checks if a secret can be deleted | **Fail** | railsapp/cssp/spec/features/free/delete_secret_spec.rb | None | 57 |
| Create secret association | checks if a secret can be associated with a user/group/ami | **Fail** | railsapp/cssp/spec/features/free/create_secret_association.rb | None | 58 |
| Edit secret | checks if the information related to a secret can be changed | **Fail** | railsapp/cssp/spec/features/free/edit_secret_spec.rb | None | 56 |
| List groups | checks if all existing groups can be listed | **Fail** | railsapp/cssp/spec/features/free/list_groups_spec.rb | None | 15 |
| List users | checks if all existing users can be listed | **Fail** | railsapp/cssp/spec/features/free/list_users_spec.rb | None | 10 |
| Remove user from group | checks if a user can be removed from a group | **Fail** | railsapp/cssp/spec/features/free/remove_user_from_group_spec.rb | None | 21 |
| Remove user | checks if a user account can be deleted | **Fail** | railsapp/cssp/spec/features/free/remove_user_spec.rb | None | 14 |
| View secrets | checks if all existing secrets can be displayed | **Fail** | railsapp/cssp/spec/features/free/view_secrets_spec.rb | None | 53 |
| Edit secret association | checks if the secret and instructions to it can be changed | **Fail** | railsapp/cssp/spec/features/free/edit_secret_association_spec.rb | None | 59 |
| Unassociate secret | checks if a secret can be unassociated with a user, group, or instance | **Fail** | railsapp/cssp/spec/features/free/unassociate_secret_spec.rb | None | 60 |

#### **Not Free Tests**

A list of all tests that **cost money** to run (i.e., tests make calls to the AWS API).

| Name | Purpose | Status | File Path | Notes | Use Case IDS |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Associate instance to group | checks if an instance can be associated with a group | **Fail** | railsapp/cssp/spec/features/not_free/associate_instance(s)_with_group_spec.rb | None | 29 |
| Associate instance to user | checks if an instance can be associated with a user | **Fail** | railsapp/cssp/spec/features/not_free/associate_instance(s)_with_user_spec.rb | None | 28 |
| Auto-stop instances | checks if all instances are stopped based on a predetermined time | **Fail** | railsapp/cssp/spec/features/not_free/auto_stop_instances_spec.rb | None | 33 |
| Create instance for user | checks if an instance can be created and associated with a user | **Pass** | railsapp/cssp/spec/features/not_free/create_instance_for_user_spec.rb | None | 35 |
| Create instance for group | checks if an instance can be created and associated with a group | **Pass** | railsapp/cssp/spec/features/not_free/create_instance_for_group_spec.rb | None | 36 |
| Create instance from AMI | checks if an instance can be created from an AMI id | **Fail** | railsapp/cssp/spec/features/not_free/create_instance_AMI_spec.rb | None | 37 |
| Create AMI | checks if an image can be created from an existing instance | **Fail** | railsapp/cssp/spec/features/not_Free/create_ami_spec.rb | None | 24 |
| Create security group | checks if a security group of a VPC can be created | **Fail** | railsapp/cssp/spec/features/not_free/create_security_group_spec.rb | None | 45 |
| Create inbound rule | checks if an inbound rule for a security group can be created | **Fail** | railsapp/cssp/spec/features/not_free/create_inbound_rule_spec.rb| None | 46 |
| Create outbound rule | checks if an outbound rule for a security group can be created | **Fail** | railsapp/cssp/spec/features/not_free/create_outbound_rule_spec.rb | None | 47 |
| Create user instance from ami | checks if an instance to a user can be created from a common AMI id | **Fail** | railsapp/cssp/spec/features/not_free/create_user_instance_AMI_spec.rb | None | 37 |
| Create group instance from ami | checks if an instance to a group can be created from a common AMI id | **Fail** | railsapp/cssp/spec/features/not_free/create_group_instance_AMI_spec.rb | None | 37 |
| Create VPC | checks if a VPC can be created in AWS | **Fail** | railsapp/cssp/spec/features/not_free/create_vpc_spec.rb | UI failure | 40 |
| Delete VPC | checks if a VPC can be deleted | **Fail** | railsapp/cssp/spec/features/not_free/delete_vpc_spec.rb | None | 52 |
| List instances | checks if instances are listed correctly | **Fail** | railsapp/cssp/spec/features/not_free/list_instances_spec.rb | None | 3 |
| View instances (user) | checks if instances can be listed from a user perspective | **Fail** | railsapp/cssp/spec/features/not_free/view_instances_spec.rb | None | 22 |
| Modify VPC | checks if a VPC's information can be edited | **Fail** | railsapp/cssp/spec/features/not_free/modify_vpc_spec.rb | None | - |
| Show VPC | checks if specific details of a VPC are shown | **Fail** | railsapp/cssp/spec/features/not_free/show_VPC_spec.rb | None | 41 |
| Show associations | checks if all secret associations can be shown | **Fail** | railsapp/cssp/spec/features/not_free/show_associations_spec.rb | None | 54 |
| Start instance | checks if an instance can be started | **Fail** | railsapp/cssp/spec/features/not_free/start_instance_spec.rb | None | 25 |
| Stop instance | checks if an instance can be stopped | **Fail** | railsapp/cssp/spec/features/not_free/stop_instance_spec.rb | None | 26 |
| Unassociate instance from group | checks if an instance can be unassociated from a group | **Fail** | railsapp/cssp/spec/features/not_free/unassociate_instance(s)_with_group_spec.rb | None | 32 |
| Unassociate instance from user | checks if an instance can be unassociated from a user | **Fail** | railsapp/cssp/spec/features/not_free/unassociate_instance(s)_with_user_spec.rb | None | 31 |
| View images | checks if common images as well as images created from instances can be displayed | **Fail** | railsapp/cssp/spec/features/not_free/view_images_spec.rb | None | 34 |
| View VPC | checks if a VPC is accessible by CSSP | **Fail** | railsapp/cssp/spec/features/not_free/view_vpc_spec.rb | None | 39 |
| Create subnet | checks if a subnet associated to a VPC can be created | **Pass** | railsapp/cssp/spec/features/not_free/create_subnet_spec.rb | Contingent on correct subnet entry | 42 |
| Delete subnet | checks if a subnet can be deleted | **Fail** | railsapp/cssp/spec/features/not_free/delete_subnet_spec.rb | None | 44 |
| Add IPv4/IPv6 CIDR ranges to rule | checks if CIDR ranges can be added | **Fail** | | Not complete | 48 |
| Delete IPv4/IPv6 CIDR ranges from rule | checks if CIDR ranges can be deleted | **Fail** | | Not complete | 49 |
| Add existing rule to another security group | checks if an existing rule can be added to a security group | **Fail** | | Not complete | 50 |
| Terminate Instance | checks if an instance can be terminated | **Fail** | railsapp/cssp/spec/features/not_free/delete_instance_spec.rb | None | 27 |
| Edit instance association | checks if an associated instance can be changed | **Fail** | railsapp/cssp/spec/features/not_free/edit_association_spec.rb | None | 30 |
| Edit image | checks if the description of a custom image can be changed | **Fail** | railsapp/cssp/spec/features/not_free/edit_image_spec.rb | None | 38 |

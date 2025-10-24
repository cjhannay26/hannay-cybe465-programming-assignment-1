# ☑ Comprehensive Guide to Setting up CSSP

This guide provides step-by-step instructions on setting up **CSSP (Cyber Sandbox Software Portal)** in both **development** and **production** modes using Docker. Please follow the instructions carefully to ensure a smooth setup process.

*This guide is for **Ubuntu 22.04 and up-to-date as of May 2023**.*

---

## Prerequisites

Before you begin, make sure you have Docker installed on your machine.

### 🐳 Docker Installation

1.  **Installing Docker**:
    * Install the Docker packages from the Ubuntu 22.04 Repository:
        ```bash
        apt install docker.io 
        ```
2.  **Adding Yourself to the Docker Group**:
    * Add yourself to the Docker group by running the following commands:
        ```bash
        sudo usermod aG docker $USER 
        newgrp docker 
        ```
    * Verify that you are in the Docker group by running the `groups` command. The output should include the "docker" group.
3.  **Starting, Stopping, Restarting, and Checking Docker Status**:
    * To check the Docker status, use the following command:
        ```bash
        sudo systemctl status docker 
        ```
    * To restart Docker, use:
        ```bash
        sudo systemctl restart docker 
        ```
    * To start Docker:
        ```bash
        sudo systemctl start docker 
        ```
    * To stop Docker:
        ```bash
        sudo systemctl stop docker 
        ```

---

## AWS Access Control Lists (ACLs) for IAM

This application is designed to be used with access to AWS restricted through **ACLs applied to an IAM account**[cite: 28]. [cite_start]Each ACL is designed to restrict access to the minimum number of components that an instance of CSSP would require[cite: 29]. [cite_start]Listed below are the ACLs that should be applied to the group containing the IAM user.

### AWS IAM ACL: Image Creation 

```json
{
"Version": "2012-10-17", 
"Statement": [
  {
    "Sid": "AllowCreateImage", 
    "Effect": "Allow", 
    "Action": "ec2:CreateImage", 
    "Resource": [
      "arn:aws:ec2:*::image/*", 
      "arn:aws:ec2:*:*:instance/*" 
    ]
  },
  {
    "Sid": "AllowCreateTags Only Launching", 
    "Effect": "Allow",
    "Action": [
      "ec2:CreateTags" 
    ],
    "Resource": [
      "arn:aws:ec2:*::image/*" 
    ]
  }
]
}
```
### AWS IAM ACL: Instance Creation
```json
{
"Version": "2012-10-17", [cite: 58]
"Statement": [
  {
    "Sid": "AllowRunInstances", [cite: 61]
    "Effect": "Allow", [cite: 64]
    "Action": "ec2:RunInstances", [cite: 65]
    "Resource": [
      "arn:aws:ec2:*::image/*", [cite: 67]
      "arn:aws:ec2:*::snapshot/*", [cite: 68]
      "arn:aws:ec2:*:*:subnet/*", [cite: 69]
      "arn:aws:ec2:*:*:network-interface/*", [cite: 70]
      "arn:aws:ec2:*:*:security-group/*", [cite: 71]
      "arn:aws:ec2:*:*:volume/*", [cite: 72]
      "arn:aws:ec2:*:*:instance/*", [cite: 73]
      "arn:aws:ec2:*:*:key-pair/*" [cite: 74]
    ]
  },
  {
    "Sid": "AllowRunInstances With Restrictions", [cite: 75]
    "Effect": "Allow", [cite: 76]
    "Action": [
      "ec2:CreateVolume", [cite: 78]
      "ec2:RunInstances" [cite: 79]
    ],
    "Resource": [
      "arn:aws:ec2:*::image/*", [cite: 83]
      "arn:aws:ec2:*:*:volume/*", [cite: 84]
      "arn:aws:ec2:*:*:network-interface/*", [cite: 85]
      "arn:aws:ec2:*:*:security-group/*", [cite: 86]
      "arn:aws:ec2:*:*:subnet/*", [cite: 87]
      "arn:aws:ec2:*:*:instance/*" [cite: 88]
    ],
    "Condition": { [cite: 89]
      "StringEquals": { [cite: 90]
        "aws:RequestTag/Owner": "cssp" [cite: 91]
      },
      "ForAllValues:StringEquals": { [cite: 93]
        "aws:TagKeys": [cite: 94]
          "Owner" [cite: 100]
        ]
      }
    }
  },
  {
    "Sid": "AllowCreateTags Only Launching", [cite: 103]
    "Effect": "Allow", [cite: 104]
    "Action": [
      "ec2:CreateTags" [cite: 107]
    ],
    "Resource": [
      "arn:aws:ec2:*:*:volume/*", [cite: 109]
      "arn:aws:ec2:*:*:instance/*" [cite: 110]
    ],
    "Condition": { [cite: 112]
      "StringEquals": { [cite: 113]
        "ec2:CreateAction": "RunInstances" [cite: 114]
      }
    }
  }
]
}
```
### AWS IAM ACL: Read EC2 Resources
```json
{
"Version": "2012-10-17", [cite: 120]
"Statement": [
  {
    "Sid": "AllowRead EC2Resources", [cite: 125]
    "Effect": "Allow", [cite: 126]
    "Action": "ec2:Describe", [cite: 127]
    "Resource": "*" [cite: 128]
  },
  {
    "Sid": "AllowDecodeErrors", [cite: 129]
    "Effect": "Allow", [cite: 130]
    "Action": "sts:DecodeAuthorizationMessage", [cite: 134]
    "Resource": "*" [cite: 134]
  }
]
}
```
### AWS IAM ACL: Instance & VPC Management
```json
{
"Version": "2012-10-17", [cite: 137]
"Statement": [
  {
    "Sid": "CreateResources", [cite: 140]
    "Effect": "Allow", [cite: 141]
    "Action": [
      "ec2:CreateDhcpOptions", [cite: 144]
      "ec2:CreateSecurityGroup", [cite: 145]
      "ec2:CreateInternetGateway", [cite: 146]
      "ec2:CreateNetworkAcl", [cite: 147]
      "ec2:CreateRoute", [cite: 148]
      "ec2:CreateRouteTable", [cite: 149]
      "ec2:CreateSubnet", [cite: 150]
      "ec2:CreateVpc", [cite: 151]
      "ec2:CreateNetworkInterface", [cite: 152]
      "ec2:ImportKeyPair" [cite: 153]
    ],
    "Resource": "*" [cite: 154]
  },
  {
    "Sid": "ModifyRoutes", [cite: 157]
    "Effect": "Allow", [cite: 158]
    "Action": [
      "ec2:CreateRoute", [cite: 160]
      "ec2:DeleteRoute" [cite: 161]
    ],
    "Resource": "arn:aws:ec2:*:*:route-table/*", [cite: 163]
    "Condition": { [cite: 164]
      "StringEquals": { [cite: 165]
        "ec2:ResourceTag/Owner": "cssp" [cite: 170]
      }
    }
  },
  {
    "Sid": "ModifyResources", [cite: 173]
    "Effect": "Allow", [cite: 174]
    "Action": [
      "ec2:DetachNetworkInterface", [cite: 177]
      "ec2:DetachInternetGateway", [cite: 178]
      "ec2:Disassociate Route Table", [cite: 179]
      "ec2:DisassociateSubnetCidrBlock", [cite: 180]
      "ec2:AssociateRouteTable", [cite: 181]
      "ec2:AssociateSubnetCidrBlock", [cite: 182]
      "ec2:ModifyVpcAttribute", [cite: 183]
      "ec2:ModifySubnetAttribute", [cite: 184]
      "ec2:DeleteNetworkAclEntry", [cite: 185]
      "ec2:CreateNetworkAclEntry", [cite: 186]
      "ec2:DeleteKeyPair", [cite: 187]
      "ec2:DescribeKeyPairs", [cite: 188]
      "ec2:ModifyInstanceAttribute", [cite: 189]
      "ec2:ModifyNetworkInterfaceAttribute" [cite: 190]
    ],
    "Resource": "*" [cite: 191]
  },
  {
    "Sid": "AllowModifyInstances", [cite: 192]
    "Effect": "Allow", [cite: 193]
    "Action": [
      "ec2:TerminateInstances", [cite: 195]
      "ec2:StartInstances", [cite: 196]
      "ec2:StopInstances", [cite: 197]
      "ec2:RebootInstances", [cite: 198]
      "ec2:DeleteVolume" [cite: 199]
    ],
    "Resource": "*", [cite: 201]
    "Condition": { [cite: 202]
      "ForAnyValue:StringEquals": { [cite: 203]
        "ec2:ResourceTag/Owner": "cssp" [cite: 209]
      }
    }
  },
  {
    "Sid": "AllowAttachIGW", [cite: 211]
    "Effect": "Allow", [cite: 212]
    "Action": "ec2:AttachInternetGateway", [cite: 213]
    "Resource": "*" [cite: 214]
  },
  {
    "Sid": "AllowDeleteWithTags", [cite: 215]
    "Effect": "Allow", [cite: 216]
    "Action": [
      "ec2:DeleteInternetGateway", [cite: 218]
      "ec2:DeleteSecurityGroup", [cite: 219]
      "ec2:DeleteDhcpOptions", [cite: 220]
      "ec2:DeleteNetworkAcl", [cite: 221]
      "ec2:DeleteRouteTable", [cite: 222]
      "ec2:DeleteRoute" [cite: 223]
    ],
    "Resource": "*", [cite: 225]
    "Condition": { [cite: 226]
      "ForAnyValue:StringEquals": { [cite: 227]
        "ec2:ResourceTag/Owner": "cssp" [cite: 231]
      }
    }
  },
  {
    "Sid": "AllowDelete Subnet", [cite: 233]
    "Effect": "Allow", [cite: 234]
    "Action": [
      "ec2:DeleteNetworkInterface", [cite: 236]
      "ec2:DeleteSubnet" [cite: 237]
    ],
    "Resource": "*" [cite: 243]
  },
  {
    "Sid": "AllowDeleteVPC", [cite: 244]
    "Effect": "Allow", [cite: 245]
    "Action": "ec2:DeleteVpc", [cite: 246]
    "Resource": "*" [cite: 247]
  },
  {
    "Sid": "AllowCreateTags", [cite: 248]
    "Effect": "Allow", [cite: 249]
    "Action": "ec2:CreateTags", [cite: 250]
    "Resource": [
      "arn:aws:ec2:*:*:subnet/*", [cite: 252]
      "arn:aws:ec2:*:*:route-table/*", [cite: 253]
      "arn:aws:ec2:*:*:dhcp-options/*", [cite: 254]
      "arn:aws:ec2:*:*:security-group/*", [cite: 255]
      "arn:aws:ec2:*:*:network-acl/*", [cite: 256]
      "arn:aws:ec2:*:*:vpc/*", [cite: 257]
      "arn:aws:ec2:*:*:instance/*", [cite: 258]
      "arn:aws:ec2:*:*:internet-gateway/*" [cite: 259]
    ]
  },
  {
    "Sid": "AuthorizeSecurity GroupAllowances", [cite: 263]
    "Effect": "Allow", [cite: 264]
    "Action": [
      "ec2:AuthorizeSecurity Group Egress", [cite: 266]
      "ec2:AuthorizeSecurity GroupIngress", [cite: 267]
      "ec2:Revoke Security Group Egress", [cite: 268]
      "ec2:RevokeSecurity GroupIngress" [cite: 269]
    ],
    "Resource": "*", [cite: 271]
    "Condition": { [cite: 272]
      "ForAnyValue:StringEquals": { [cite: 273]
        "ec2:ResourceTag/Owner": "cssp" [cite: 278]
      }
    }
  }
]
}
```
## Setting up CSSP in Development Mode

### Running the Application

1.  **Building the Container**:
    * Navigate to the `~/capstone-cssp/docker/cssp-dev` directory.
    * Execute the following command to build the container `CSSP-dev`:
        ```bash
        ./build-container.sh
        ```
2.  **Creating Google OAuth2 Keys (Optional)**:
    * These steps are for the utilization of Google OAuth2 in development mode and are derived from the official documentation at Setting up OAuth 2.0 - API Console Help
    * Go to the Google API Console.
    * Select a project or create a new one from the projects list.
    * Click on "**Credentials**" on the left side.
    * Create credentials and select "**OAuth client ID**".
    * Set the "**Application type**" to "**Web application**" and specify the desired application name.
    * Click "**+ ADD URI**" under "**Authorized redirect URIs**".
    * Set the value to:
        ```
        http://localhost:3000/users/auth/google_oauth2/callback
        ```
    * Click "**Create**" and make note of the **Client ID** and **Client secret**.
3.  **Creating AWS Access Keys**:
    * This step is necessary to restrict AWS access through ACLs applied to an IAM account.
    * Apply the required ACLs to the group containing the IAM user.
4.  **Setting up the Environment Variables**:
    * Navigate to the `~/capstone-cssp/docker/cssp-dev` directory.
    * Create a file for environment variables by copying the template:
        ```bash
        cp secretsTemplate.env secrets.env
        ``` 
    * Fill out the `secrets.env` file using your preferred text editor. Provide the required information such as admin email, admin password, AWS access keys, region, tenant ID, and Google API keys.
5.  **Starting the Container and the Server**:
    * Execute the following command to start the container:
        ```bash
        ./start-container.sh
        ```
    * CSSP should now be accessible at **http://localhost:3000/**.
6.  **Restarting the Container**:
    * If the container exists in the exited state, follow these steps to restart it.
    * Navigate to the `~/capstone-cssp/docker/cssp-dev` directory.
    * Run the following command to restart the container:
        ```bash
        ./restart-container.sh
        ```
7.  **Entering the Application Container**:
    * If you would like to access the application container while it is running, follow these steps.
    * Navigate to the `~/capstone-cssp/docker/cssp-dev` directory.
    * Run the following command to enter the container:
        ```bash
        ./enter-container.sh
        ```
    * You will now be inside the container within a **Bash Shell**.
8.  **Viewing the Database**:
    * If you wish to view the database behind Active Record, you have two options:
    * **Option 1: Terminal**
        * Install SQLite3 using the following command:
            ```bash
            apt install sqlite3
            ```
        * Use the following command to view the database:
            ```bash
            sqlite3 ~/capstone-cssp/railsapp/cssp/db/development.sqlite3
            ```
    * **Option 2: GUI**
        * Install SQLiteBrowser using the following command:
            ```bash
            apt install sqlitebrowser
            ```
        * Use the following command to view the database:
            ```bash
            sqlitebrowser ~/capstone-cssp/railsapp/cssp/db/development.sqlite3
            ```
*Congratulations! You have successfully set up and deployed CSSP in development mode. [cite_start]The application is now accessible at http://localhost:3000/.*

---

## Setting up CSSP in Production Mode

### Considerations Before Proceeding

1.  **Domain/Hosts File**:
    * If you are hosting the application without a domain, you need to add an entry to your `/etc/hosts` file.
    * Open the file and add the following line: `your_ip cssp.wvu.com`, replacing `your_ip` with the appropriate IP address.
    * If you wish to use a different domain name, edit the production environment file located at `~/capstone-cssp/railsapp/cssp/config/environments/production.rb`.
    * Within this file, locate the line that controls the supported hosts for the webpage and add the desired domain.
    * Make sure the route in `/etc/hosts` matches the domain used in this line.
2.  **HTTPS Keys**:
    * If you prefer to use your own key and certificate for HTTPS, place your key (renamed to `server.key`) and certificate (named `server.crt`) within the `~/capstone-cssp/railsapp/cssp` directory.

### Running the Application

1.  **Building the Container**:
    * Navigate to the `~/capstone-cssp/docker/cssp-prod` directory.
    * Execute the following command to build the container `cssp-prod`:
        ```bash
        ./build-container.sh
        ```
2.  **Creating Google OAuth2 Keys**:
    * These steps are required for configuring Google OAuth2 in production mode.
    * Go to the Google API Console.
    * Select a project or create a new one from the projects list.
    * Click on "**Credentials**" on the left side.
    * Create credentials and select "**OAuth client ID**".
    * Set the "**Application type**" to "**Web application**" and provide the desired application name.
    * Click "**+ ADD URI**" under "**Authorized redirect URIs**".
    * Set the value to `https://your_domain/users/auth/google_oauth2/callback`, replacing `your_domain` with the hosts value set in the production environment file.
    * Click "**Create**" and make note of the **Client ID** and **Client secret**.
3.  **Creating AWS Access Keys**:
    * Ensure that your AWS access is restricted through ACLs applied to an IAM account.
    * Apply the appropriate ACLs to the group containing the IAM user.
4.  **Setting up the Environment Variables**:
    * Navigate to the `~/capstone-cssp/docker/cssp-prod` directory.
    * Create a file for environment variables by copying the template:
        ```bash
        cp secretsTemplate.env secrets.env
        ```
    * Fill out the `secrets.env` file using a text editor of your choice. Provide the required information, such as the default admin email, instance length, AWS access keys, region, tenant ID, and Google API keys.
5.  **Starting the Server**:
    * Execute the following command to start the container:
        ```bash
        ./start-container.sh
        ```
    * CSSP should now be accessible at **`https://your_domain/`**, where `your_domain` corresponds to the hosts value set in the production environment file.
6.  **Restarting the Container**:
    * If the container is in the exited state, follow these steps to restart it.
    * Navigate to the `~/capstone-cssp/docker/cssp-prod` directory.
    * Run the following command to restart the container:
        ```bash
        ./restart-container.sh
        ```
7.  **Entering the Application Container**:
    * If you would like to access the application container while it is running, follow these steps.
    * Navigate to the `~/capstone-cssp/docker/cssp-prod` directory.
    * Run the following command to enter the container:
        ```bash
        ./enter-container.sh
        ```
    * You will now be inside the container within a **Bash Shell**.
8.  **Viewing the Database**:
    * a. Ensure that the container with the web server is running.
    * b. Navigate to the `~/capstone-cssp/docker/cssp-prod` directory.
    * c. Enter the container by executing the following command:
        ```bash
        ./enter-container.sh
        ```
    * d. Once inside the container's Bash shell, run the following command to access the database:
        ```bash
        sqlite3 db/production.sqlite3
        ```
    * e. You can now view and interact with the database using SQLite commands (e.g., retrieving data from tables, perform queries, or update records).
    * **Note:** Exercise caution when modifying the database to avoid unintended consequences. It's recommended to have a backup of the database before making any changes.

*Congratulations! You have successfully set up and deployed CSSP in production mode. The application is now accessible at https://your_domain/.*

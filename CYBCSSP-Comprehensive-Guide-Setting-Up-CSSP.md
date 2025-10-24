## Setting up CSSP in Development Mode

### Running the Application

1.  **Building the Container**:
    * [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-dev` directory[cite: 283].
    * [cite_start]Execute the following command to build the container `CSSP-dev`[cite: 284]:
        ```bash
        ./build-container.sh
        ```
2.  **Creating Google OAuth2 Keys (Optional)**:
    * [cite_start]Go to the Google API Console[cite: 289].
    * [cite_start]Select a project or create a new one from the projects list[cite: 290].
    * [cite_start]Click on "**Credentials**" on the left side[cite: 291].
    * [cite_start]Create credentials and select "**OAuth client ID**"[cite: 292].
    * [cite_start]Set the "**Application type**" to "**Web application**" and specify the desired application name[cite: 293].
    * [cite_start]Click "**+ ADD URI**" under "**Authorized redirect URIs**"[cite: 294].
    * Set the value to:
        ```
        http://localhost:3000/users/auth/google_oauth2/callback
        [cite_start]``` [cite: 296]
    * [cite_start]Click "**Create**" and make note of the **Client ID** and **Client secret**[cite: 297].
3.  **Creating AWS Access Keys**:
    * [cite_start]This step is necessary to restrict AWS access through ACLs applied to an IAM account[cite: 299].
    * [cite_start]Apply the required ACLs to the group containing the IAM user[cite: 300].
4.  **Setting up the Environment Variables**:
    * [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-dev` directory[cite: 302].
    * [cite_start]Create a file for environment variables by copying the template[cite: 303]:
        ```bash
        cp secretsTemplate.env secrets.env
        [cite_start]``` [cite: 304]
    * Fill out the `secrets.env` file using your preferred text editor. [cite_start]Provide the required information such as admin email, admin password, AWS access keys, region, tenant ID, and Google API keys[cite: 305, 306].
5.  **Starting the Container and the Server**:
    * [cite_start]Execute the following command to start the container[cite: 308, 309]:
        ```bash
        ./start-container.sh
        ```
    * [cite_start]CSSP should now be accessible at **http://localhost:3000/**[cite: 310, 334].
6.  **Restarting the Container**:
    * [cite_start]If the container exists in the exited state, follow these steps to restart it[cite: 312].
    * [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-dev` directory[cite: 313].
    * [cite_start]Run the following command to restart the container[cite: 314, 315]:
        ```bash
        ./restart-container.sh
        ```
7.  **Entering the Application Container**:
    * [cite_start]If you would like to access the application container while it is running, follow these steps[cite: 317].
    * [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-dev` directory[cite: 318].
    * [cite_start]Run the following command to enter the container[cite: 319, 320]:
        ```bash
        ./enter-container.sh
        ```
    * [cite_start]You will now be inside the container within a **Bash Shell**[cite: 321].
8.  **Viewing the Database**:
    * [cite_start]If you wish to view the database behind Active Record, you have two options[cite: 323]:
    * **Option 1: Terminal**
        * [cite_start]Install SQLite3 using the following command[cite: 325, 326]:
            ```bash
            apt install sqlite3
            ```
        * [cite_start]Use the following command to view the database[cite: 327, 328]:
            ```bash
            sqlite3 ~/capstone-cssp/railsapp/cssp/db/development.sqlite3
            ```
    * **Option 2: GUI**
        * [cite_start]Install SQLiteBrowser using the following command[cite: 330, 331]:
            ```bash
            apt install sqlitebrowser
            ```
        * [cite_start]Use the following command to view the database[cite: 332, 333]:
            ```bash
            sqlitebrowser ~/capstone-cssp/railsapp/cssp/db/development.sqlite3
            ```
*Congratulations! You have successfully set up and deployed CSSP in development mode. [cite_start]The application is now accessible at http://localhost:3000/[cite: 334].*

---

## Setting up CSSP in Production Mode

### Considerations Before Proceeding

1.  **Domain/Hosts File**:
    * [cite_start]If you are hosting the application without a domain, you need to add an entry to your `/etc/hosts` file[cite: 338].
    * [cite_start]Open the file and add the following line: `your_ip cssp.wvu.com`, replacing `your_ip` with the appropriate IP address[cite: 339, 340].
    * [cite_start]If you wish to use a different domain name, edit the production environment file located at `~/capstone-cssp/railsapp/cssp/config/environments/production.rb`[cite: 341].
    * [cite_start]Within this file, locate the line that controls the supported hosts for the webpage and add the desired domain[cite: 342].
    * [cite_start]Make sure the route in `/etc/hosts` matches the domain used in this line[cite: 343].
2.  **HTTPS Keys**:
    * [cite_start]If you prefer to use your own key and certificate for HTTPS, place your key (renamed to `server.key`) and certificate (named `server.crt`) within the `~/capstone-cssp/railsapp/cssp` directory[cite: 344].

### Running the Application

1.  **Building the Container**:
    * [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-prod` directory[cite: 347].
    * [cite_start]Execute the following command to build the container `cssp-prod`[cite: 348, 349]:
        ```bash
        ./build-container.sh
        ```
2.  **Creating Google OAuth2 Keys**:
    * [cite_start]These steps are required for configuring Google OAuth2 in production mode[cite: 351].
    * [cite_start]Go to the Google API Console[cite: 353].
    * [cite_start]Select a project or create a new one from the projects list[cite: 354].
    * [cite_start]Click on "**Credentials**" on the left side[cite: 355].
    * [cite_start]Create credentials and select "**OAuth client ID**"[cite: 356].
    * [cite_start]Set the "**Application type**" to "**Web application**" and provide the desired application name[cite: 357].
    * [cite_start]Click "**+ ADD URI**" under "**Authorized redirect URIs**"[cite: 358].
    * [cite_start]Set the value to `https://your_domain/users/auth/google_oauth2/callback`, replacing `your_domain` with the hosts value set in the production environment file[cite: 360, 361].
    * [cite_start]Click "**Create**" and make note of the **Client ID** and **Client secret**[cite: 362].
3.  **Creating AWS Access Keys**:
    * [cite_start]Ensure that your AWS access is restricted through ACLs applied to an IAM account[cite: 364].
    * [cite_start]Apply the appropriate ACLs to the group containing the IAM user[cite: 365].
4.  **Setting up the Environment Variables**:
    * [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-prod` directory[cite: 367].
    * [cite_start]Create a file for environment variables by copying the template[cite: 368, 369]:
        ```bash
        cp secretsTemplate.env secrets.env
        ```
    * [cite_start]Fill out the `secrets.env` file using a text editor of your choice[cite: 370]. [cite_start]Provide the required information, such as the default admin email, instance length, AWS access keys, region, tenant ID, and Google API keys[cite: 371].
5.  **Starting the Server**:
    * [cite_start]Execute the following command to start the container[cite: 373, 374]:
        ```bash
        ./start-container.sh
        ```
    * [cite_start]CSSP should now be accessible at **`https://your_domain/`**, where `your_domain` corresponds to the hosts value set in the production environment file[cite: 375, 376].
6.  **Restarting the Container**:
    * [cite_start]If the container is in the exited state, follow these steps to restart it[cite: 378].
    * [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-prod` directory[cite: 379].
    * [cite_start]Run the following command to restart the container[cite: 380, 381]:
        ```bash
        ./restart-container.sh
        ```
7.  **Entering the Application Container**:
    * [cite_start]If you would like to access the application container while it is running, follow these steps[cite: 383].
    * [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-prod` directory[cite: 384].
    * [cite_start]Run the following command to enter the container[cite: 385, 386]:
        ```bash
        ./enter-container.sh
        ```
    * [cite_start]You will now be inside the container within a **Bash Shell**[cite: 387].
8.  **Viewing the Database**:
    * a. [cite_start]Ensure that the container with the web server is running[cite: 389].
    * b. [cite_start]Navigate to the `~/capstone-cssp/docker/cssp-prod` directory[cite: 390].
    * c. [cite_start]Enter the container by executing the following command[cite: 391, 392]:
        ```bash
        ./enter-container.sh
        ```
    * d. [cite_start]Once inside the container's Bash shell, run the following command to access the database[cite: 393]:
        ```bash
        sqlite3 db/production.sqlite3
        ```
    * e. [cite_start]You can now view and interact with the database using SQLite commands (e.g., retrieving data from tables, perform queries, or update records)[cite: 395, 396].
    * **Note:** Exercise caution when modifying the database to avoid unintended consequences. [cite_start]It's recommended to have a backup of the database before making any changes[cite: 397, 398].

*Congratulations! You have successfully set up and deployed CSSP in production mode. [cite_start]The application is now accessible at https://your_domain/[cite: 399].*

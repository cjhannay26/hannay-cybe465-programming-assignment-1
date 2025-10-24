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

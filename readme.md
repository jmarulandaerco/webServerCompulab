<h1 align="center">Web server for information visualization.
</h1>

<p align="center">
<img  align="center" src="./logo.png">
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
    <summary>Table of Contents</summary>
    <ol>
        <li><a href="#about-the-project">About the project</a></li>
        <li><a href="#Funcionamiento_general">General operation</a>
            <ul>
                <li><a href="#structure_project">Project structure </a></li>
                <li><a href="#app">AppFrontend</a></li>
                <li><a href="#view_frontend">View AppFrontend</a></li>
                <li><a href="#view_auth_app">Foder authApp</a></li>
                <li><a href="#energy_app">Foder energyApp</a></li>
                <li><a href="#energy_project">Folder energy proyect</a></li>
                <li><a href="#scripts">Folder Scripts (javascript)</a></li>
            </ul>
        </li>
        <li><a href="#requirements">Installation requirements </a></li>
        <li><a href="#License">License</a></li>
        <li><a href="#Derechos">Copyrights</a></li>
    </ol>
</details>



<p id="about-the-project">
</p>



## About the project

<div style="text-align:justify">

### Django Web Server for Ercopulse Configuration

An application is created with Django for both the frontend and backend, using JavaScript, CSS, and HTML.  

This web server is used to display a menu that allows the configuration of the **Ercopulse** for reading and writing data via the **Modbus protocol**.  

The main function of the web server is to display information from the **inverters**.
</div>

<p id="Funcionamiento_general">
</p>

# General operation

### Project Overview  

This project includes a `start_django.sh` file that contains a series of instructions executed by **cron** or a **Linux service** to start the Django application.  

The application takes a few seconds to start, but once running, it allows configurations that would normally be done through the **Ercopulse menu**.  

The main function is the **visualization of inverter information**, database data, and other functionalities such as viewing logs, configuring files, and managing certain functions.  

<p id="structure_project">
</p>

## Project structure


The project includes a `manage.py` file used to start the Django application. It consists of **five folders**, with the most important being `AppFrontend`, a Django app that contains three key directories:  

1. **static/** – This folder contains resources such as images, CSS files, fonts, and JavaScript scripts for the application.  
2. **templates/** – This folder holds all the HTML files, organized in subdirectories that reflect their location in the visual menu.  
3. **views/** – This folder contains the logic for retrieving, modifying, and deleting information related to the configuration of the **Ercopulse monitoring application**.  

<p id="view_frontend">
</p>

## View AppFrontend


In the `views/` folder of `AppFrontend`, there are several important files:

1. **checkPassWordView.py** – Contains the class for verifying the password to ensure the correct password is provided for making changes or accessing certain configuration options.  
2. **contentView.py** – Contains the logic for loading the templates or HTML pages onto the website.  
3. **deleteView.py** – Contains the logic for deleting event logs and database records.  
4. **homeView.py** – Contains the class that loads the homepage.  
5. **json.py** – Contains the logic for downloading data from the database in JSON format.  
6. **loginView.py** – Contains the logic for handling the login process.  
7. **logView.py** – Contains the logic for retrieving event logs. It can be updated every 5 seconds, with the option to change this time by modifying the logic in the script responsible for the update event.  
8. **menuView.py** – Contains the logic for retrieving, modifying, and creating configurations or devices. These are variable classes, but the main focus is on modifying `.ini` files.  
9. **modbusView.py** – Contains the majority of the logic related to the Modbus protocol.  
10. **modemView.py** – Contains the logic for retrieving information from the modem.  
11. **settingSystemView.py** – Contains the logic for modifying and retrieving system configuration information.

<p id="view_auth_app">
</p>

## Folder auth App

# authApp

The `authApp` is a Django application responsible for authentication and authorization. It includes the user model and its corresponding serialization. The most important folders in this app are:

1. **models** – Contains the user model.  
2. **serializers** – Contains the serializer for the user.  
3. **views** – Contains the logic for token management, login, and logout functionality of the application.

<p id="energy_app">
</p>

## Folder energy app

The third folder is `energyAPP`, which contains the model for obtaining data from the inverters along with its respective serializer. In the `views`, the logic for stopping, starting, and restarting the monitoring service is included, as well as the retrieval of data from the inverter.

<p id="energy_project">
</p>


## Folder energy project


The fourth folder is a Django project and contains the project's configurations in `settings.py`, such as the database connection, migrations, middleware, among others. The `urls.py` file defines the endpoints used for making API requests and/or loading templates.

## Folder scripts

In the `script` folder of `AppFrontend`, there are several `.js` files that function as controllers, connecting the views (HTML files) with the Python code. There are two main folders: 

- **Modbus Folder**: Contains the `modbus.js` file, which holds the logic for loading information related to Modbus, updating, and creating data.
- **Menu Folder**: Contains the `compensation_limitation.js` file, which includes functions to load information for the compensation and limitation sections.

Other important files include:
- **database.js**: This file contains the logic for interacting with the database. It includes functionalities to retrieve data, configurations, download Excel files, among others.
- **http.js**: This file contains functions for checking the modem, configuring the modem's signal, and updating the modem's service.
- **loadDatapage.js**: This file contains functions for loading the HTML files, retrieving data, passing it to different pages, and updating various configurations that can be modified.
- **logs.js**: This file contains the logic for handling `log.log`.
- **password.js**: This file includes functions for checking and changing the password in `config_to`.
- **service.js**: This file contains functions for the service status, starting, and stopping the service. It also creates a progress bar function to show the service startup time.
- **settingSystem.js**: This file contains functions for configuring system-related settings, such as Wi-Fi, Wi-Fi antenna, and Ethernet ports 1 and 2.
- **sidebar.js**: This file contains functions for downloading `.txt` files with database information and restarting the compilation process.

<p id="scripts">
</p>



<p id="requirements">
</p>


## Installation and Requirements

Please follow the steps below to properly configure your development and production environments:

1. **Configuration in `settings.py`:**

   Ensure that the following settings are present in your `settings.py` file and remain unchanged:

   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

2. **Collecting Static Files:**

After making changes to static files, run the following command in your terminal:

bash
Copiar
Editar
python manage.py collectstatic
This command gathers all static files into a directory that Django recognizes, especially when used with Gunicorn. It's important to maintain the existing folder structure and make modifications to HTML scripts as necessary.

3. **Serving Static Files with Gunicorn:**

By default, Gunicorn does not serve static files. To handle this, it's recommended to use a web server like Nginx in conjunction with Gunicorn. Nginx can serve static files directly, improving performance and efficiency. For more information on setting up Nginx with Gunicorn to serve static files, refer to this guide.

4. **Gunicorn Service:**

The Linux service managing the application is named gunicorn.service. Ensure that this service is correctly configured and running to handle application requests efficiently. For guidance on setting up Gunicorn as a service, consult the Gunicorn documentation.

## Licences

This project has been developed using **open source programming language and libraries**. No additional licenses were required for its implementation.  

<p id="Derechos" >
    
</p>

## Copyrights

All rights reserved for Erco Energy 2025.

let intervalId;


/**
 * Loads content into a specified section of the page based on the selected option.
 * 
 * This function fetches HTML content from the server corresponding to the given `option` and injects it into the `content2` element on the page. If the content loads successfully, it also calls the `loadFunction` for further processing based on the selected option. If an error occurs during the fetch or while loading the content, an error message is displayed in the `content2` section.
 * 
 * @param {string} option - The option that determines which content to load. This value is used to construct the URL `/home/content/form/${option}/` from which the content is fetched.
 * 
 * @returns {void} This function does not return a value. It updates the `content2` section with the fetched HTML content.
 * 
 * @throws {Error} If the fetch request fails or the content cannot be loaded, an error message is shown in the `content2` section of the page.
 * 
 * @example
 * loadContentMenu('databaseSetting'); // Loads the content for the 'databaseSetting' option and processes it.
 */

function loadContentMenu(option) {
    fetch(`/home/content/form/${option}/`)
        .then(response => {
            if (!response.ok) {
                alert(`Error loading content: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content2").innerHTML = data;
            loadFunction(option);

        })
        .catch(error => {
            document.getElementById("content2").innerHTML = "<h1>Error loading content</h1>";
        });
}

/**
 * Loads content into a specified section of the page based on the selected option.
 * 
 * This function fetches HTML content from the server corresponding to the given `option` and injects it into the `content2` element on the page. If the content loads successfully, it also calls the `loadFunction` for further processing based on the selected option. If an error occurs during the fetch or while loading the content, an error message is displayed in the `content2` section.
 * 
 * @param {string} option - The option that determines which content to load. This value is used to construct the URL `/home/content/form/setting/${option}/` from which the content is fetched.
 * 
 * @returns {void} This function does not return a value. It updates the `content5` section with the fetched HTML content.
 * 
 * @throws {Error} If the fetch request fails or the content cannot be loaded, an error message is shown in the `content5` section of the page.
 * 
 * @example
 * loadContentSetting('databaseSetting'); // Loads the content for the 'databaseSetting' option and processes it.
 */

function loadContentSetting(option) {
    fetch(`/home/content/form/setting/${option}/`)
        .then(response => {
            if (!response.ok) {
                alert(`Error loading content: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content5").innerHTML = data;

        })
        .catch(error => {
            document.getElementById("content5").innerHTML = "<h1>Error loading content</h1>";
        });
}
/**
 * Dynamically loads content into the page based on the provided option.
 * 
 * This function makes a GET request to fetch HTML content from the server using the specified `option`. The content is then inserted into the `content4` section of the page. If the fetch request is successful, it calls `loadFunction` with the selected option for further processing. In case of errors, an error message is displayed within the `content4` section.
 * 
 * @param {string} option - The type of content to load, which is appended to the URL `/home/content/form/checker/${option}/` to fetch the corresponding HTML content from the server.
 * 
 * @returns {void} This function does not return any value. It modifies the `content4` section of the page by inserting the fetched content or displaying an error message.
 * 
 * @throws {Error} If the fetch request fails or the content cannot be loaded, an error message will be displayed in the `content4` section.
 * 
 * @example
 * loadContentHttp('checkerStatus'); // Loads content related to 'checkerStatus' and triggers `loadFunction` for further actions.
 */

function loadContentHttp(option) {
    fetch(`/home/content/form/checker/${option}/`)
        .then(response => {
            if (!response.ok) {
                alert(`Error loading content: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content4").innerHTML = data;
            loadFunction(option);

        })
        .catch(error => {
            document.getElementById("content4").innerHTML = "<h1>Error loading content</h1>";
        });
}
/**
 * Loads form data for the logging settings from the server and populates the form fields.
 * 
 * This asynchronous function makes a `GET` request to fetch logging configuration data from the server. Upon receiving the response, it populates the corresponding form fields with values from the response data. If the request is unsuccessful, an error message is displayed to the user.
 * 
 * @returns {void} This function does not return any value. It modifies the form fields within the page by filling them with the data fetched from the server.
 * 
 * @throws {Error} If the fetch request fails or the server returns an error, the user will be alerted with a message indicating that the data loading has failed.
 * 
 * @example
 * loadFormDataSettingLog(); // Loads the logging settings and fills in the corresponding form fields.
 */

async function loadFormDataSettingLog() {
    try {
        const response = await fetch(getFormDatasettingLog);
        if (!response.ok) {
            alert("Error loading the data");
        }
        const data = await response.json();
        document.getElementById("level").value = data.level;
        document.getElementById("stdout").value = data.stdout;
        document.getElementById("file").value = data.file;
        document.getElementById("enable").value = data.enable;
        document.getElementById("log_size").value = data.log_size;
        document.getElementById("backup").value = data.backup;

    } catch (error) {
        console.error("Error:", error);
    }
}

/**
 * Updates the logging settings on the server with the data entered in the form.
 * 
 * This asynchronous function sends a `PUT` request to the server with the logging configuration data from the form. It includes the values for `level`, `stdout`, `file`, `enable`, `log_size`, and `backup`. If the update is successful, the user is alerted with a success message. If there is an error, the user is alerted with an error message.
 * 
 * @returns {void} This function does not return any value. It performs an update operation and provides feedback to the user via alerts.
 * 
 * @throws {Error} If the fetch request fails or the server returns an error, the user will be alerted with an error message.
 * 
 * @example
 * updateInformationDataSettingLog(); // Updates the logging settings with the form values.
 */


async function updateInformationDataSettingLog() {
    const level = document.getElementById("level").value;
    const stdout = document.getElementById("stdout").value;
    const file = document.getElementById("file").value;
    const enable = document.getElementById("enable").value;
    const log_size = document.getElementById("log_size").value;
    const backup = document.getElementById("backup").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        const response = await fetch(getFormDatasettingLog, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ level, stdout, file, enable, log_size, backup })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation"); 

        } else {
            alert("✅ " + data.message); 


        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};

/**
 * Loads the interface settings data from the server and populates the form fields.
 * 
 * This asynchronous function sends a `GET` request to the server to retrieve the current interface settings. The retrieved data is used to populate the values of the `interface` and `connection` fields in the form. If the request is unsuccessful, an error message is shown to the user.
 * 
 * @returns {void} This function does not return any value. It performs the loading operation and updates the form with the retrieved data.
 * 
 * @throws {Error} If the fetch request fails or the server returns an error, the user will be alerted with an error message.
 * 
 * @example
 * loadFormDataSettingInterface(); // Loads the interface settings and populates the form fields.
 */


async function loadFormDataSettingInterface() {
    try {
        const response = await fetch(getFormDataUrlSettingInterface);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();
        document.getElementById("interface").value = data.interface;
        document.getElementById("connection").value = data.connection;
    } catch (error) {
        console.error("Error:", error);
    }
}

/**
 * Updates the interface settings by sending the new values to the server.
 * 
 * This asynchronous function collects the current values of the interface and connection form fields, and sends them to the server using a `PUT` request to update the interface settings. It includes CSRF protection by sending the CSRF token along with the request. Upon success, the user is alerted with a success message. If the request fails, an error message is shown.
 * 
 * @returns {void} This function does not return any value. It sends the updated settings to the server and displays appropriate messages based on the response.
 * 
 * @throws {Error} If the fetch request fails or the server returns an error, an alert with an error message is shown to the user.
 * 
 * @example
 * updateSettingInterface(); // Updates the interface settings with the values from the form fields.
 */


async function updateSettingInterface() {
    const interface = document.getElementById("interface").value;
    const connection = document.getElementById("connection").value;


    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        const response = await fetch(getFormDataUrlSettingInterface, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ interface, connection})
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation"); 

        } else {
            alert("✅ " + data.message); 


        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};

/**
 * Loads the signal checker form data from the server and populates the form fields.
 * 
 * This asynchronous function sends a request to the server to retrieve signal checker settings. Upon receiving the data, it populates the form fields with the values of `onomondo` and `minimum` from the response. If the data cannot be loaded due to an error or invalid response, an error alert is shown. Any errors encountered during the request are logged to the console.
 * 
 * @returns {void} This function does not return any value. It populates the form with the signal checker data upon successful retrieval.
 * 
 * @throws {Error} If the fetch request fails or the server response is invalid, an error is logged to the console.
 * 
 * @example
 * loadFormDataSignalChecker(); // Loads and populates the signal checker settings form with data from the server.
 */

async function loadFormDataSignalChecker() {
    try {
        const response = await fetch(getFormDataSignalChecker);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();
        document.getElementById("onomondo").value = data.onomondo;
        document.getElementById("minimum").value = data.minimum;
    } catch (error) {
        console.error("Error:", error);
    }
}
/**
 * Loads the modem checker form data from the server and populates the form fields.
 * 
 * This asynchronous function sends a request to the server to retrieve modem checker settings. Upon receiving the data, it populates the form fields with the values of `connection` and `attemts` from the response. If the data cannot be loaded due to an error or invalid response, an error alert is shown. Any errors encountered during the request are logged to the console.
 * 
 * @returns {void} This function does not return any value. It populates the form with the modem checker data upon successful retrieval.
 * 
 * @throws {Error} If the fetch request fails or the server response is invalid, an error is logged to the console.
 * 
 * @example
 * loadFormDataModemChecker(); // Loads and populates the modem checker settings form with data from the server.
 */


async function loadFormDataModemChecker() {
    try {
        const response = await fetch(getFormDataModemChecker);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();
        document.getElementById("connection").value = data.connection;
        document.getElementById("attemts").value = data.attemts;
    } catch (error) {
        console.error("Error:", error);
    }
}

/**
 * Loads the server checker form data from the server and populates the form field.
 * 
 * This asynchronous function sends a request to the server to retrieve server checker settings. Upon receiving the data, it populates the form field with the value of `requests` from the response. If the data cannot be loaded due to an error or invalid response, an error alert is shown. Any errors encountered during the request are logged to the console.
 * 
 * @returns {void} This function does not return any value. It populates the form with the server checker data upon successful retrieval.
 * 
 * @throws {Error} If the fetch request fails or the server response is invalid, an error is logged to the console.
 * 
 * @example
 * loadFormDataServerChecker(); // Loads and populates the server checker settings form with data from the server.
 */


async function loadFormDataServerChecker() {
    try {
        const response = await fetch(getFormDataServerChecker);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();
        document.getElementById("requests").value = data.requests;
    } catch (error) {
        console.error("Error:", error);
    }
}


async function loadFormDataAwsSettings() {
    try {
        const response = await fetch(awsSttings);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();
        document.getElementById("requests").value = data.requests;
    } catch (error) {
        console.error("Error:", error);
    }
}

/**
 * Dynamically loads content into the main content area based on the specified option.
 * 
 * This function determines the URL to fetch content from based on the `option` parameter. It populates the main content area with the retrieved data and triggers specific actions based on the selected option. If the option corresponds to logs, it sets up periodic refreshes and event listeners. Additionally, the active state of sidebar links is updated based on the selected option.
 * 
 * @param {string} option - The identifier for the content to load. This can correspond to different sections or forms in the application.
 * 
 * @returns {void} This function does not return any value. It manipulates the DOM to update the content and the sidebar, and triggers specific actions like fetching logs or loading form data.
 * 
 * @throws {Error} If an error occurs during the fetch operation (e.g., network failure or invalid response), an error message is displayed in the content area, and the error is logged to the console.
 * 
 * @example
 * loadContent('form/database/database'); // Loads the database form content and triggers related functions.
 */


function loadContentSingleDevice(option) {
    document.querySelector('.container_logs').style.display = 'none';
    document.getElementById('content3').style.display = 'block';


    url=`/home/content/${option}/`
    fetch(url)
        .then(response => {
            if (!response.ok) {
                alert(`Error loading content: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content3").innerHTML = data;
            loadFunction(option);

        })
        .catch(error => {
            document.getElementById("content3").innerHTML = "<h1>Error loading content</h1>";
        });
}


function loadContent(option) {
    console.log("Terirr");
    if(option=='form/database/database'){
        url='/home/content/form/database/databaseInformation/'

    }
   
    else{
        url=`/home/content/${option}/`
    }
    fetch(url)
        .then(response => {
            if (!response.ok) {
                alert(`Error when loading content: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content").innerHTML = data;

            switch (option) {
                case "form/compensation-limitation/limitation":
                    loadFormDataLimitation();
                    break;

                case "form/compensation-limitation/compensation":
                    loadFormDataCompensation();
                    break;

                case "form/database/databaseSetting":
                    loadFormDataBase();
                    break;
                
            }

            if (option === "logs") {

                document.getElementById("refreshButton").addEventListener("click", fetchLogs);

                intervalId = setInterval(fetchLogs, 5000);

            } else {
                if (intervalId) {
                    clearInterval(intervalId);
                    intervalId = null; 
                }
            }

            document.querySelectorAll("#sidebar a").forEach(a => a.classList.remove("active"));


            document.querySelectorAll("#sidebar a").forEach(a => {
                if (a.getAttribute("onclick")?.includes(option)) {
                    a.classList.add("active");
                }
            });
        })
        .catch(error => {
            console.log(error)
            document.getElementById("content").innerHTML = "<h1>Error when loading content</h1>";
        });
}

/**
 * Loads server selection form data from a specified URL and populates the corresponding form fields.
 * 
 * This asynchronous function fetches server selection data from a provided endpoint and updates the form fields with the returned data. The fields updated include `server`, `neu_plus`, `telemetry`, `mqtt`, and `storage`. If an error occurs while fetching or processing the data, an error message is logged to the console.
 * 
 * @returns {void} This function does not return any value. It updates the DOM by setting the values of specific form elements.
 * 
 * @throws {Error} If the fetch operation fails (e.g., network error, invalid response), an error message is logged to the console.
 * 
 * @example
 * loadFormDataServerSelection(); // Fetches data and populates the server selection form fields.
 */


async function loadFormDataServerSelection() {
    try {
        const response = await fetch(getFormDataUrlServerSelection);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();

        document.getElementById("server").value = data.server;
        document.getElementById("neu_plus").value = data.neu_plus;
        document.getElementById("telemetry").value = data.telemetry;
        document.getElementById("mqtt").value = data.mqtt;
        document.getElementById("storage").value = data.storage;
    } catch (error) {
        console.error("Error:", error);
    }
}

/**
 * Updates the server selection settings by sending the form data to the server.
 * 
 * This asynchronous function gathers data from the server selection form fields and sends it to the server using a PUT request. The form fields include `server`, `neu_plus`, `telemetry`, `mqtt`, and `storage`. If the request is successful, the server's response message is displayed. If there is an error (either from the server or the network), an error message is shown to the user.
 * 
 * @returns {void} This function does not return any value. It triggers updates to the server configuration via a PUT request.
 * 
 * @throws {Error} If the fetch operation fails (e.g., network error, invalid response), an error message is logged to the console, and a user-facing alert is shown.
 * 
 * @example
 * updateServerSelection(); // Sends updated server settings to the server.
 */

async function updateServerSelection() {
    const server = document.getElementById("server").value;
    const neu_plus = document.getElementById("neu_plus").value;
    const telemetry = document.getElementById("telemetry").value;
    const mqtt = document.getElementById("mqtt").value;
    const storage = document.getElementById("storage").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        const response = await fetch(getFormDataUrlServerSelection, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ server, neu_plus, telemetry, mqtt, storage })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation");

        } else {
            alert("✅ " + data.message); 


        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};

/**
 * Loads and displays the data for the database page, fetching the data from the API with pagination.
 * 
 * This function fetches the data from the server based on the current page and the number of items to display per page. It then updates the content of the page with the retrieved data. While the data is being fetched, a loading message is displayed. If an error occurs during the fetch operation, an error message is shown to the user.
 * 
 * @param {number} page - The current page number to load from the server. This is used for pagination.
 * 
 * @returns {void} This function does not return any value. It updates the page's content with the fetched data.
 * 
 * @throws {Error} If the fetch operation fails (e.g., network issue, invalid response), an error message is shown to the user.
 * 
 * @example
 * loadDatabase(1); // Loads the data for the first page with the default number of items per page.
 */


function loadDatabase(page) {
    console.log("Función loadDatabase ejecutada");  // Mensaje de depuración
    console.log(page)
    const perPageSelect = document.getElementById('perPageSelect');
    const perPage = perPageSelect ? perPageSelect.value : 10; // Valor predeterminado: 10
    const fullUrl = `/api/inverter/status/?page=${page}&per_page=${perPage}`;

    const contentElement = document.getElementById("content");

    // Mostrar mensaje de carga mientras se hace la petición
    contentElement.innerHTML = "<p>Cargando datos...</p>";

    fetch(fullUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            return response.text();
        })
        .then(html => {
            contentElement.innerHTML = html; // Actualiza el contenido de la página
        })
        .catch(error => {
            console.error("Error al cargar los datos:", error);
            contentElement.innerHTML = `<p>Error al cargar los datos: ${error.message}</p>`;
        });
}


/**
 * Saves the changes for enabling or disabling selected devices based on user input.
 * 
 * This function gathers the devices that the user has selected through checkboxes, sends the selected devices
 * to the server via a PUT request to update their status (enable/disable). It handles CSRF protection via a token
 * and displays success or error messages based on the server response.
 * 
 * @returns {void} This function does not return any value. It performs a PUT request to the server to update device status.
 * 
 * @throws {Error} If the fetch operation fails, or the response from the server is invalid, an error message is shown.
 * 
 * @example
 * saveChangesEnableDisableDevices(); // Sends the selected devices to the server for enabling/disabling.
 */


async function saveChangesEnableDisableDevices() {
    const selectedDevices = Array.from(document.querySelectorAll('input[name="devices"]:checked'))
                                .map(checkbox => checkbox.value);

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 
    
    try {
        const response = await fetch(viewDevices, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ selectedDevices })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation"); 

        } else {
            alert("✅ " + data.message); 


        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
    }
    
}

/**
 * Loads different forms or functions based on the given option.
 * 
 * This function handles the loading of various forms or functions based on the specified `option` value.
 * The function uses a switch statement to determine which form or function to load. Each case corresponds to a 
 * specific `option` and triggers the appropriate form data loader or handler.
 * 
 * @param {string} option - The identifier for the form or function to be loaded.
 * 
 * @returns {void} This function does not return any value. It calls other functions to load data or initialize forms.
 * 
 * @throws {Error} This function does not throw errors but will silently skip unrecognized options.
 * 
 * @example
 * loadFunction('modbusMeasure'); // Loads the form data related to Modbus measurement.
 */


async function loadFunction(option) {
    switch (option) {
        case 'modbusMeasure':
            loadFormDataMeasureModbus();
            break;
        case 'serverSelectionModbus':
            loadFormDataServerSelection();
            break;
        case 'operationModeModbus':
            loadFormDataModes();
            break;
        case 'databaseSetting':
            loadFormDataSettingDatabase();
            break;
        case 'networkSettings':
            loadFormDataSettingInterface();
            break;
        case 'advanced':
            loadFormDataAdvanced();
            break;
        case 'settingLog':
            loadFormDataSettingLog();
            break;
        case 'modemChecker':
            loadFormDataModemChecker();
            break;
        case 'serverChecker':
            loadFormDataServerChecker();
            break;
        case 'signalChecker':
            loadFormDataSignalChecker();
            break;
        case 'registerDeviceRtu':
            loadAddDevices();
            break;
        case 'modbusSetting':
            loadFormDataSettingModbus();
            break
        case 'registerDeviceTcp':
            loadAddDevices();
        case 'registerDeviceRtu':
            loadAddDevices();
        case 'modifyRtu':
            break;
        case 'modifyTcp':
            break;
        case 'awsService':
            loadFormDataAwsSettings();
            break;
   
        default:
            break;

    }

}
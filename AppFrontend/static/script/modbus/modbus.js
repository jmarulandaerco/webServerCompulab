/**
 * Loads content dynamically from the server based on the provided option 
 * and updates the HTML of the "content3" element. Also invokes a specified 
 * function based on the option parameter.
 *
 * @param {string} option - The option used to determine which content to load 
 *                           from the server (e.g., a specific form or data set).
 *
 * This function performs the following:
 * - Sends a fetch request to the server to load content from a URL constructed 
 *   using the provided `option`.
 * - If the request is successful, it updates the inner HTML of the element with 
 *   ID "content3" with the loaded data.
 * - If an error occurs during the fetch or response processing, it shows an error 
 *   message in the "content3" element and alerts the user.
 * - It also calls a function (`loadFunction`) with the `option` passed as an argument.
 *
 * @example
 * loadContentModbus("config");
 */

function loadContentModbus(option) {
    fetch(`/home/content/form/modbus/${option}/`)
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

/**
 * Fetches and loads a list of devices from the API and displays the results in the "content3" element.
 *
 * This function constructs the full URL for the API endpoint by appending the `page` parameter to the 
 * device query string. It then fetches the data from the server, handles the response, and updates the
 * content of the HTML element with the id "content3" with the received HTML. If there is an error during 
 * the fetch request, it logs the error and updates the "content3" element with an error message.
 *
 * @param {string} page - The page number or identifier to be passed in the query string to the API.
 * 
 * @returns {void}
 */

function loadDevices(page) {
    const fullUrl = `/api/modbus/devices/?device=${encodeURIComponent(page)}`; 
    fetch(fullUrl)  
        .then(response => {
            console.log(response);
            if (!response.ok) {
                alert(`Error: ${response.statusText}`);
            }
            return response.text();
        })
        .then(html => {
            document.getElementById("content3").innerHTML = html;
        })
        .catch(error => {
            console.error("Error while loading devices:", error);
            document.getElementById("content3").innerHTML = "<p>Error while loading devices</p>";
        });
}


/**
 * Asynchronously loads form data for Modbus settings from the server and populates 
 * the form fields with the received data. If an error occurs, an alert is shown.
 *
 * This function performs the following:
 * - Sends a fetch request to the server to retrieve Modbus settings data in JSON format.
 * - If the request is successful, it populates the form fields (`debug`, `attempts`, `timeout`) 
 *   with the corresponding values from the server response.
 * - If the request fails or the response is not successful, an error message is shown to the user.
 * - If there is an error during the fetch process, it catches the error and alerts the user.
 *
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the form fields are populated or an error is handled.
 *
 * @example
 * loadFormDataSettingModbus();
 */

async function loadFormDataSettingModbus() {
    try {
        const response = await fetch(getFormDatasettingModbus);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();
        document.getElementById("debug").value = data.debug;
        document.getElementById("attempts").value = data.attempts;
        document.getElementById("timeout").value = data.timeout;
    } catch (error) {
        alert("Error:", error);
    }
}

/**
 * Handles the change event of the Modbus map folder selection. It sends the selected value to the server, 
 * retrieves a list of Modbus map options, and updates the Modbus map JSON dropdown with the available options.
 *
 * This function performs the following:
 * - Retrieves the selected value from the Modbus map folder dropdown (`modbus_map_folder`).
 * - Sends a POST request to the server with the selected value in the request body.
 * - On a successful response, populates the Modbus map JSON dropdown (`modbus_map_json`) with the available options.
 * - If there are options available, it sets the first option as the selected value and triggers a change event.
 * - If an error occurs during the fetch process, it displays an error message in the `content3` element.
 *
 * @param {Event} event - The change event triggered when the Modbus map folder selection changes.
 *
 * @example
 * handleSelectChange(event);
 */
function handleSelectChange(event) {
    const modbusMapFolderSelect = document.getElementById("modbus_map_folder");
    const selectedValue = modbusMapFolderSelect.value;  
    fetch(mapFolder, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"

        },
        body: JSON.stringify({ selectedValue })

    })
        .then(response => response.json())
        .then(data => {
          
            const modbusMapList = data.data;

            const modbusMapFolderSelect = document.getElementById("modbus_map_json");

            modbusMapFolderSelect.innerHTML = "";

            modbusMapList.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.value = option;
                optionElement.textContent = option;
                modbusMapFolderSelect.appendChild(optionElement);
            });

            if (modbusMapList.length > 0) {
                modbusMapFolderSelect.value = modbusMapList[0];

                modbusMapFolderSelect.dispatchEvent(new Event("change"));
            }


        }).catch(error => {
            document.getElementById("content3").innerHTML = "<h1>Error loading content</h1>";
        });
}


/**
 * Loads the available Modbus map options from the server and updates the Modbus map folder dropdown. 
 * It selects the appropriate device based on the provided `selectedDevice` parameter.
 *
 * This function performs the following:
 * - Sends a fetch request to the server to retrieve a list of available Modbus maps.
 * - Populates the Modbus map folder dropdown (`modbus_map_folder`) with the available options.
 * - If a `selectedDevice` is provided and exists in the Modbus map list, it sets that device as the selected value.
 * - If no device is selected or available, the first Modbus map is selected by default.
 * - If no devices are available, it shows an alert informing the user.
 * - Dispatches a "change" event on the Modbus map dropdown to trigger any dependent actions.
 * - In case of an error, logs the error in the console.
 *
 * @param {string} [selectedDevice] - The device to pre-select in the dropdown, if it exists in the list.
 *
 * @example
 * loadAddDevicesUpdateDevice("device1");
 */

function loadAddDevicesUpdateDevice(selectedDevice) {
    fetch(mapFolder)
        .then(response => {
            if (!response.ok) {
                alert(`Error: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const modbusMapList = data.modbus_map;
            const modbusMapFolderSelect = document.getElementById("modbus_map_folder");

            modbusMapFolderSelect.innerHTML = "";

            modbusMapList.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.value = option;
                optionElement.textContent = option;
                modbusMapFolderSelect.appendChild(optionElement);
            });

            if (selectedDevice && modbusMapList.includes(selectedDevice)) {
                modbusMapFolderSelect.value = selectedDevice;
            } else if (modbusMapList.length > 0) {
                modbusMapFolderSelect.value = modbusMapList[0];
            } else {
                alert("❌ No devices are available for selection.");
            }

            modbusMapFolderSelect.dispatchEvent(new Event("change"));
        })
        .catch(error => {
            console.error("Error while loading devices:", error);
        });
}


/**
 * Loads the available Modbus map options from the server and populates the Modbus map folder dropdown.
 * If devices are available, the first device is selected by default and a "change" event is triggered.
 *
 * This function performs the following:
 * - Sends a fetch request to the server to retrieve a list of available Modbus map options.
 * - Clears the existing options in the Modbus map folder dropdown (`modbus_map_folder`).
 * - Populates the dropdown with the retrieved Modbus map options.
 * - If options are available, selects the first device and triggers a "change" event on the dropdown.
 * - If an error occurs during the fetch process, it alerts the user with the error message.
 *
 * @example
 * loadAddDevices();
 */


function loadAddDevices() {
    fetch(mapFolder)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const modbusMapList = data.modbus_map;  // Aquí obtenemos la lista de opciones

            const modbusMapFolderSelect = document.getElementById("modbus_map_folder");

            modbusMapFolderSelect.innerHTML = "";

            modbusMapList.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.value = option;  // El valor del "option" será el nombre del dispositivo
                optionElement.textContent = option;  // El texto visible será el nombre del dispositivo
                modbusMapFolderSelect.appendChild(optionElement);
            });
            if (modbusMapList.length > 0) {
                modbusMapFolderSelect.value = modbusMapList[0];

                modbusMapFolderSelect.dispatchEvent(new Event("change"));
            }
        })
        .catch(error => {
            alert("Error while loading devices:", error);
        });
}
/**
 * Asynchronously loads measurement data for Modbus from the server and populates the form fields with the retrieved data.
 * If an error occurs during the fetch process, it logs the error to the console and alerts the user.
 *
 * This function performs the following:
 * - Sends a fetch request to the server to retrieve measurement data in JSON format.
 * - Populates the form fields (`zone`, `modbus`, `start`, `stop`) with the corresponding values from the server response.
 * - If an error occurs during the fetch operation or if the response is not successful, an alert is shown.
 * - In case of any fetch errors, the error is logged to the console.
 *
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the form fields are populated with data or an error is handled.
 *
 * @example
 * loadFormDataMeasureModbus();
 */

async function loadFormDataMeasureModbus() {
    try {
        const response = await fetch(getFormDataUrl);
        if (!response.ok) {
            alert("Error while loading devices");
        }
        const data = await response.json();
        document.getElementById("zone").value = data.zone;
        document.getElementById("modbus").value = data.modbus;
        document.getElementById("start").value = data.start;
        document.getElementById("stop").value = data.stop;
    } catch (error) {
        console.error("Error:", error);
    }
}

/**
 * Asynchronously sends an update request to the server to modify Modbus settings with the provided form data.
 * It includes CSRF protection by sending the CSRF token with the request. If the update is successful, 
 * it shows an alert with the success message; if it fails, it shows an error message.
 *
 * This function performs the following:
 * - Retrieves the values from the form fields (`debug`, `attempts`, `timeout`) to be updated.
 * - Sends a PUT request to the server with the form data in JSON format and includes the CSRF token in the request headers.
 * - If the response is successful, an alert is shown with the success message returned from the server.
 * - If the request fails, it shows an error message in the alert and logs the error in the console.
 *
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the update request is completed and the alert is shown.
 *
 * @example
 * updateSettingModbus();
 */

async function updateSettingModbus() {
    const log_debug = document.getElementById("debug").value;
    const max_attempts = document.getElementById("attempts").value;
    const timeout_attempts = document.getElementById("timeout").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        const response = await fetch(getFormDatasettingModbus, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ log_debug, max_attempts, timeout_attempts })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation"); // Muestra éxito si las contraseñas coinciden

        } else {
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden


        }

    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};


/**
 * Asynchronously sends an update request to modify measurement settings for Modbus with the provided form data.
 * The function includes CSRF protection by sending the CSRF token with the request. It shows an alert based on
 * the success or failure of the update.
 *
 * This function performs the following:
 * - Retrieves the values from the form fields (`zone`, `modbus`, `start`, `stop`) to be updated.
 * - Sends a PUT request to the server with the data in JSON format, including the CSRF token in the request headers.
 * - If the response is successful, an alert with the success message returned from the server is shown.
 * - If the request fails, an alert with an error message is displayed and the error is logged in the console.
 *
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the update request is completed and an alert is shown.
 *
 * @example
 * updateMeasureModbus();
 */


async function updateMeasureModbus() {
    const zone = document.getElementById("zone").value;
    const modbus = document.getElementById("modbus").value;
    const start = document.getElementById("start").value;
    const stop = document.getElementById("stop").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(getFormDataUrl, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ zone, modbus, start, stop })
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
 * Asynchronously loads mode settings data from the server and populates the form fields based on the retrieved data.
 * It retrieves settings related to mode, limitation, compensation, and sampling from the server and updates
 * the corresponding form elements.
 *
 * This function performs the following:
 * - Sends a fetch request to the server to retrieve mode data in JSON format.
 * - Populates the mode field with the value received from the server.
 * - Sets the corresponding limitation and compensation radio buttons to the values from the server.
 * - Fills the sampling fields (`sampling_limitation`, `sampling_compensation`) with the corresponding data from the server.
 * - If the fetch request fails, an error is logged in the console.
 *
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the form is populated with the fetched data or logs an error.
 *
 * @example
 * loadFormDataModes();
 */

async function loadFormDataModes() {
    try {
        const response = await fetch(getFormDataUrlServerModes);
        if (!response.ok) {
            alert("Error while loading data");
        }
        const data = await response.json();

        document.getElementById("mode").value = data.mode;

        const limitationRadio = document.querySelector(`input[name="limitation"][value="${data.limitation}"]`);
        if (limitationRadio) {
            limitationRadio.checked = true;
        }

        const compensationRadio = document.querySelector(`input[name="compensation"][value="${data.compensation}"]`);
        if (compensationRadio) {
            compensationRadio.checked = true;
        }

        // Llenar los campos de sampling
        document.getElementById("sampling_limitation").value = data.sampling_limitation;
        document.getElementById("sampling_compensation").value = data.sampling_compensation;
    } catch (error) {
        console.error("Error:", error);
    }
}


/**
 * Asynchronously sends an update request to modify mode settings based on the form data.
 * The function includes CSRF protection by sending the CSRF token with the request.
 * It shows an alert based on the success or failure of the update.
 *
 * This function performs the following:
 * - Retrieves the values from the form fields (`mode`, `limitation`, `compensation`, `sampling_limitation`, `sampling_compensation`).
 * - Sends a PUT request to the server with the collected data in JSON format, including the CSRF token in the request headers.
 * - If the response is successful, it shows an alert with the success message returned from the server.
 * - If the request fails, an alert with an error message is shown and the error is logged to the console.
 *
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the update request is completed and an alert is shown.
 *
 * @example
 * updateDataModes();
 */


async function updateDataModes() {
    const mode = document.getElementById("mode").value;
    const limitation = document.querySelector('input[name="limitation"]:checked')?.value;
    const compensation = document.querySelector('input[name="compensation"]:checked')?.value;
    const sampling_limitation = document.getElementById("sampling_limitation").value;
    const sampling_compensation = document.getElementById("sampling_compensation").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        const response = await fetch(getFormDataUrlServerModes, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ mode, limitation, compensation, sampling_limitation, sampling_compensation })
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
 * Asynchronously adds a new RTU device by sending the device's configuration data to the server.
 * The function sends a POST request with the form data to the server, including a CSRF token for protection.
 * It shows an alert based on the success or failure of the operation.
 *
 * This function performs the following:
 * - Retrieves the configuration values for the new RTU device from the form fields.
 * - Sends a POST request to the server with the device data in JSON format and includes the CSRF token in the request headers.
 * - If the response is successful, it shows a success message and calls `loadDevices` to refresh the device list.
 * - If the request fails, it shows an error message with the validation issue returned by the server.
 *
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the device is added successfully or an error is displayed.
 *
 * @example
 * addDeviceRtu();
 */

async function addDeviceRtu() {
    try {
        const nameDevice = document.getElementById("name").value;
        const portDevice = document.getElementById("port").value;
        const baudrate = document.getElementById("baudrate").value;
        const initial = document.getElementById("initial").value;
        const end = document.getElementById("end").value;
        const modbus_function = document.getElementById("modbus_function").value;
        const initial_address = document.getElementById("initial_address").value;
        const total_registers = document.getElementById("total_registers").value;
        const modbus_map_folder = document.getElementById("modbus_map_folder").value;
        const modbus_map_json = document.getElementById("modbus_map_json").value;
        const modbus_mode = document.getElementById("modbus_mode").value;
        const device_type = document.getElementById("device_type").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const save_db = document.getElementById("save_db").value;
        const server_send = document.getElementById("server_send").value;

        const response = await fetch(viewAddRtu, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                nameDevice, portDevice, baudrate, initial, end, modbus_function,
                initial_address, total_registers, modbus_map_folder, modbus_map_json,
                modbus_mode, device_type, save_db, server_send
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            await loadDevices('seeDevices');
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}

/**
 * Asynchronously adds a new TCP device by sending the device's configuration data to the server.
 * The function sends a POST request with the device data in JSON format, including a CSRF token for security.
 * Based on the response, it shows either a success or error message.
 *
 * This function performs the following actions:
 * - Retrieves the configuration values for the new TCP device from the form fields.
 * - Sends a POST request to the server with the device data and includes the CSRF token for security.
 * - If the request is successful, it displays a success message and refreshes the list of devices by calling `loadDevices`.
 * - If the request fails, it displays an error message with the issue returned from the server.
 *
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the device is added or an error is displayed.
 *
 * @example
 * addDeviceTcp();
 */

async function addDeviceTcp() {
    try {
        const nameDevice = document.getElementById("name").value;
        const ip_device = document.getElementById("ip_device").value;
        const port_device = document.getElementById("port_device").value;
        const offset = document.getElementById("offset").value;
        const initial = document.getElementById("initial").value;
        const end = document.getElementById("end").value;
        const modbus_function = document.getElementById("modbus_function").value;
        const initial_address = document.getElementById("initial_address").value;
        const total_registers = document.getElementById("total_registers").value;
        const modbus_map_folder = document.getElementById("modbus_map_folder").value;
        const modbus_map_json = document.getElementById("modbus_map_json").value;
        const modbus_mode = document.getElementById("modbus_mode").value;
        const device_type = document.getElementById("device_type").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const save_db = document.getElementById("save_db").value;
        const server_send = document.getElementById("server_send").value;

        const response = await fetch(viewAddTcp, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                nameDevice, ip_device, port_device, offset, initial, end, modbus_function,
                initial_address, total_registers, modbus_map_folder, modbus_map_json,
                modbus_mode, device_type, save_db, server_send
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            await loadDevices('seeDevices');
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}

/**
 * Asynchronously deletes a device by sending a DELETE request to the server with the device data.
 * The function asks for confirmation from the user before proceeding with the deletion.
 * If confirmed, it sends a DELETE request to the server and shows either a success or error message.
 *
 * This function performs the following actions:
 * - Prompts the user to confirm the deletion of the device.
 * - If the user confirms, it sends a DELETE request to the server with the device data.
 * - If the request is successful, it displays a success message and reloads the device list by calling `loadDevices`.
 * - If the request fails, it displays an error message returned from the server.
 *
 * @async
 * @function
 * @param {Object} device - The device object to be deleted.
 * @returns {Promise<void>} A promise that resolves when the device is deleted or an error is displayed.
 *
 * @example
 * deleteDevice(device);
 */


async function deleteDevice(device) {
    try {
        console.log(device)
        if (confirm("Are you sure to erase the device?")) {
            const response = await fetch(mapFolder, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ device })
            });

            const result = await response.json();

            if (!response.ok) {
                alert("❌ Error in validation: " + result.message);
            } else {
                alert("✅ " + result.message);
                await loadDevices('seeDevices');
            }
        }
    } catch (error) {
        console.error("Error in deletion:", error.message);
    }
}

/**
 * Asynchronously modifies the device options (RTU or TCP) by fetching the appropriate form and updating the fields 
 * based on the device type (RTU or TCP). The function dynamically loads the corresponding data and pre-fills the form.
 * It updates the device configuration fields for either RTU or TCP devices depending on the selected device type.
 *
 * This function performs the following:
 * - Determines the device type (RTU or TCP) and fetches the corresponding form for modification.
 * - Loads the form data based on the device type and populates the fields with the device-specific details.
 * - If the device is RTU, it fetches additional data for RTU configuration and updates the corresponding fields.
 * - If the device is TCP, it fetches additional data for TCP configuration and updates the corresponding fields.
 * - It also calls the `loadAddDevices` and `loadAddDevicesUpdateDevice` functions to handle additional device-related operations.
 * 
 * @async
 * @function
 * @param {string} device - The identifier of the device (RTU or TCP) to modify.
 * @returns {Promise<void>} A promise that resolves when the form is updated with the device data.
 * 
 * @example
 * ModifyOption("RTU_001");
 */


async function ModifyOption(device) {
    try {
        let url = device.includes("RTU")
            ? "/home/content/form/modbus/updateDeviceRtu/"
            : "/home/content/form/modbus/updateDeviceTcp/";

        const response = await fetch(url);

        if (!response.ok) {
            alert("❌ Error in validation: " + response.message);
        }

        const data = await response.text();
        document.getElementById("content3").innerHTML = data;
        loadAddDevices();

        if (device.includes("RTU")) {
            const responseDevice = await fetch(`${modifyDevice}?device=${encodeURIComponent(device)}`);


            if (!responseDevice.ok) {
                alert(" ❌ Error while loading the data device Rtu");
            }
            const dataRtu = await responseDevice.json();
            document.getElementById("nameRtu").value = dataRtu.nameRtu;
            document.getElementById("portRtu").value = dataRtu.portRtu;
            document.getElementById("baudrateRtu").value = dataRtu.baudrateRtu;
            document.getElementById("initialRtu").value = dataRtu.initialRtu;
            document.getElementById("endRtu").value = dataRtu.endRtu;
            document.getElementById("modbus_function_rtu").value = dataRtu.modbus_function_rtu;
            document.getElementById("initial_address_rtu").value = dataRtu.initial_address_rtu;
            document.getElementById("total_registers_rtu").value = dataRtu.total_registers_rtu;
            document.getElementById("modbus_map_folder").value = dataRtu.modbus_map_folder_rtu;
            loadAddDevicesUpdateDevice(dataRtu.modbus_map_folder_rtu)
            document.getElementById("modbus_map_json").value = dataRtu.modbus_map_json_rtu;
            document.getElementById("modbus_mode_rtu").value = dataRtu.modbus_mode_rtu;
            document.getElementById("device_type_rtu").value = dataRtu.device_type_rtu;
            document.getElementById("save_db_rtu").value = dataRtu.save_db_rtu;
            document.getElementById("server_send_rtu").value = dataRtu.server_send_rtu;
        } else {
            const responseDevice = await fetch(`${modifyDevice}?device=${encodeURIComponent(device)}`);


            if (!responseDevice.ok) {
                alert(" ❌  Error while loading the data device Rtu");
            }
            const dataRtu = await responseDevice.json();
            document.getElementById("nameTcp").value = dataRtu.nameTcp;
            document.getElementById("ip_device_tcp").value = dataRtu.ip_device_tcp;
            document.getElementById("port_device_tcp").value = dataRtu.port_device_tcp;
            document.getElementById("offset_tcp").value = dataRtu.offset_tcp;
            document.getElementById("initial_tcp").value = dataRtu.initial_tcp;
            document.getElementById("end_tcp").value = dataRtu.end_tcp;
            document.getElementById("modbus_function_tcp").value = dataRtu.modbus_function_tcp;
            document.getElementById("initial_address_tcp").value = dataRtu.initial_address_tcp;
            document.getElementById("total_registers_tcp").value = dataRtu.total_registers_tcp;
            document.getElementById("modbus_map_folder").value = dataRtu.modbus_map_folder_tcp;
            loadAddDevicesUpdateDevice(dataRtu.modbus_map_folder_tcp)
            document.getElementById("modbus_map_json").value = dataRtu.modbus_map_json_tcp;
            document.getElementById("modbus_mod_tcp").value = dataRtu.modbus_mod_tcp;
            document.getElementById("device_type_tcp").value = dataRtu.device_type_tcp;
            document.getElementById("save_db_tcp").value = dataRtu.save_db_tcp;
            document.getElementById("server_send_tcp").value = dataRtu.server_send_tcp;


        }


    } catch (error) {
        document.getElementById("content3").innerHTML = "<h1>Error al cargar el contenido</h1>";
    }
}


/**
 * Asynchronously updates the configuration of a TCP device by sending a PUT request to the server.
 * The function collects the current values from the input fields in the form, sends them as a JSON payload to the server, 
 * and handles the server response to confirm if the update was successful or if there was an error.
 *
 * This function performs the following:
 * - Collects data from various form fields (e.g., name, IP, port, Modbus function, etc.) to create a request payload.
 * - Sends a PUT request to update the TCP device configuration.
 * - Displays an alert indicating success or failure based on the server's response.
 * - Refreshes the device list by calling `loadDevices` if the update is successful.
 * 
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the device configuration is updated and the devices list is reloaded.
 * 
 * @example
 * updateDeviceTcp();
 */

async function updateDeviceTcp() {
    try {
        const nameDevice = document.getElementById("nameTcp").value;
        const ip_device = document.getElementById("ip_device_tcp").value;
        const port_device = document.getElementById("port_device_tcp").value;
        const offset = document.getElementById("offset_tcp").value;
        const initial = document.getElementById("initial_tcp").value;
        const end = document.getElementById("end_tcp").value;
        const modbus_function = document.getElementById("modbus_function_tcp").value;
        const initial_address = document.getElementById("initial_address_tcp").value;
        const total_registers = document.getElementById("total_registers_tcp").value;
        const modbus_map_folder = document.getElementById("modbus_map_folder").value;
        const modbus_map_json = document.getElementById("modbus_map_json").value;
        const modbus_mode = document.getElementById("modbus_mod_tcp").value;
        const device_type = document.getElementById("device_type_tcp").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const save_db = document.getElementById("save_db_tcp").value;
        const server_send = document.getElementById("server_send_tcp").value;

        const response = await fetch(viewAddTcp, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                nameDevice, ip_device, port_device, offset, initial, end, modbus_function,
                initial_address, total_registers, modbus_map_folder, modbus_map_json,
                modbus_mode, device_type, save_db, server_send
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            await loadDevices('seeDevices');
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}


/**
 * Asynchronously updates the configuration of an RTU (Remote Terminal Unit) device by sending a PUT request to the server.
 * The function collects the current values from the RTU device configuration form, sends them as a JSON payload to the server,
 * and handles the server response to confirm if the update was successful or if there was an error.
 *
 * This function performs the following:
 * - Collects data from various form fields (e.g., name, port, baudrate, Modbus function, etc.) to create a request payload.
 * - Sends a PUT request to update the RTU device configuration.
 * - Displays an alert indicating success or failure based on the server's response.
 * - Refreshes the device list by calling `loadDevices` if the update is successful.
 * 
 * @async
 * @function
 * @returns {Promise<void>} A promise that resolves when the RTU device configuration is updated and the devices list is reloaded.
 * 
 * @example
 * updateDeviceRtu();
 */


async function updateDeviceRtu() {
    try {
        const nameDevice = document.getElementById("nameRtu").value;
        const portDevice = document.getElementById("portRtu").value;
        const baudrate = document.getElementById("baudrateRtu").value;
        const initial = document.getElementById("initialRtu").value;
        const end = document.getElementById("endRtu").value;
        const modbus_function = document.getElementById("modbus_function_rtu").value;
        const initial_address = document.getElementById("initial_address_rtu").value;
        const total_registers = document.getElementById("total_registers_rtu").value;
        const modbus_map_folder = document.getElementById("modbus_map_folder").value;
        const modbus_map_json = document.getElementById("modbus_map_json").value;
        const modbus_mode = document.getElementById("modbus_mode_rtu").value;
        const device_type = document.getElementById("device_type_rtu").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const save_db = document.getElementById("save_db_rtu").value;
        const server_send = document.getElementById("server_send_rtu").value;

        const response = await fetch(viewAddRtu, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                nameDevice, portDevice, baudrate, initial, end, modbus_function,
                initial_address, total_registers, modbus_map_folder, modbus_map_json,
                modbus_mode, device_type, save_db, server_send
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            await loadDevices('seeDevices');
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}



async function readDeviceRtu() {
    try {
        const typeComunication = "RTU"
        const portDevice = document.getElementById("port_rtu").value;
        const baudrate = document.getElementById("baudrate_rtu").value;
        const attempts = document.getElementById("attempts_rtu").value;
        const timeout = document.getElementById("timeout_rtu").value
        const idSlave = document.getElementById("slave_rtu").value;
        const modbus_function = document.getElementById("modbus_function_rtu").value;
        const initial_address = document.getElementById("initial_address_rtu").value;
        const total_registers = document.getElementById("total_registers_rtu").value;
        
        const response = await fetch(logRtu, {
            method: "PUT",
          
            body: JSON.stringify({
                typeComunication,portDevice,baudrate,attempts,timeout,idSlave,modbus_function,initial_address,total_registers
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            getLogSingleDevice();
            
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}



async function readDeviceTcp() {
    try {
        const typeComunication = "TCP"
        const host = document.getElementById("ip_device_tcp").value;
        const port = document.getElementById("port_device_tcp").value;
        const attempts = document.getElementById("attempts_tcp").value;
        const timeout = document.getElementById("timeout_tcp").value
        const idSlave = document.getElementById("slave_tcp").value;
        const modbus_function = document.getElementById("modbus_function_tcp").value;
        const initial_address = document.getElementById("initial_address_tcp").value;
        const total_registers = document.getElementById("total_registers_tcp").value;
        
        const response = await fetch(logTcp, {
            method: "PUT",
           
            
            body: JSON.stringify({
                typeComunication,host,port,attempts,timeout,idSlave,modbus_function,initial_address,total_registers
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            getLogSingleDevice();   
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}
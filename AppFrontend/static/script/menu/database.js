/**
 * Sends updated database configuration settings to the server via a PUT request.
 * 
 * This asynchronous function collects the database configuration values (host, port, name, timeout, and date) 
 * from the form inputs in the DOM and sends them to the server using a PUT request. It includes a CSRF token in the 
 * request headers for security. The function handles the server response by displaying a success or error message 
 * based on the server's response.
 * 
 * @async
 * @function
 * 
 * @returns {void} This function does not return a value but shows an alert message based on the result of the request.
 * 
 * @throws {Error} If the fetch operation or server response fails, the function will log the error and display an alert.
 * 
 * @example
 * updateInformationDatabase(); // Sends updated database settings and shows a success or error message.
 */

async function updateInformationDatabase() {
    const host = document.getElementById("host").value;
    const port = document.getElementById("port").value;
    const name = document.getElementById("name").value;
    const timeout = document.getElementById("timeout").value;
    const date = document.getElementById("date").value;
    const send_average_measure = Array.from(document.querySelectorAll('input[name="average_measure"]:checked'))
        .map(checkbox => checkbox.value);
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    try {
        const response = await fetch(getFormDataBase, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ host, port, name, timeout, date,send_average_measure})
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401){
                localStorage.removeItem('access_token');
                window.location.href = "{% url 'index' %}"; 

            }
            alert("❌ " + "Error en la validación de los datos: " + data.message);

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        // console.error("Error:", error);
    }
};
/**
 * Loads the database settings and populates the form fields with the data from the server.
 * 
 * This asynchronous function makes a GET request to the server to retrieve the current database settings, 
 * including `day` and `awaitTime`. Upon successful response, it populates the respective form fields in the DOM
 * with the data. If there is an error during the request or if the server response is not successful, an alert is shown.
 * 
 * @async
 * @function
 * 
 * @returns {void} This function does not return a value but updates the form fields with the retrieved data.
 * 
 * @throws {Error} If the fetch operation or server response fails, the function will log the error to the console.
 * 
 * @example
 * loadFormDataSettingDatabase(); // Fetches database settings and updates the form with the retrieved values.
 */




async function loadFormDataSettingDatabase() {
    try {
        const response = await fetch(getFormDataUrlSettingDatabase);
        if (!response.ok) {
            alert("Error cargando data");
        }
        const data = await response.json();
        document.getElementById("day").value = data.day;
        document.getElementById("awaitTime").value = data.awaitTime;
    } catch (error) {
        // console.error("Error:", error);
    }
}

/**
 * Updates the database settings by sending the values of the form fields to the server.
 * 
 * This asynchronous function retrieves the current values of the `day` and `awaitTime` fields from the form,
 * and sends them to the server using a PUT request. The request includes a CSRF token for security. If the server
 * successfully processes the request, an alert with a success message is shown. Otherwise, an error message is displayed.
 * 
 * @async
 * @function
 * 
 * @returns {void} This function does not return a value but sends a PUT request to the server to update the database settings.
 * 
 * @throws {Error} If the fetch operation or server response fails, the function will alert the user with an error message 
 * and log the error to the console.
 * 
 * @example
 * updateSettingDatabase(); // Sends the updated database settings to the server.
 */


async function updateSettingDatabase() {
    const day = document.getElementById("day").value;
    const awaitTime = document.getElementById("awaitTime").value;


    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(getFormDataUrlSettingDatabase, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ day, awaitTime })
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401){
                localStorage.removeItem('access_token');
                window.location.href = "{% url 'index' %}"; 

            }
            alert("❌ " + "Error en la validación de los datos: " + data.message);

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        // console.error("Error:", error);
    }
};


/**
 * Exports data to an Excel file by initiating a download.
 * 
 * This function triggers the download of data from a specified type ('inverter', 'weather', 'power', or 'fault')
 * in Excel format. The file name is generated dynamically with the current timestamp.
 * 
 * @param {string} type - The type of data to export ('inverter', 'weather', 'power', 'fault').
 * 
 * @returns {void}
 */
function exportToExcel(type) {
    const boton = document.getElementById("refreshButton");
    if (boton) boton.disabled = true;

    const now = new Date();
    const dateString = now.toISOString().replace(/[-:.]/g, ''); // 'YYYYMMDDHHMMSS'

    let filenamePrefix = '';
    switch (type) {
        case 'inverter':
            filenamePrefix = 'investor_data';
            break;
        case 'weather':
            filenamePrefix = 'weather_data';
            break;
        case 'power':
            filenamePrefix = 'power_data';
            break;
        case 'fault':
            filenamePrefix = 'fault_data';
            break;
        default:
            console.error('Tipo de exportación no válido');
            if (boton) boton.disabled = false;
            return;
    }

    const a = document.createElement('a');
    a.href = `/api/${type}/export/`;
    a.download = `${filenamePrefix}${dateString}.xlsx`;
    a.click();

    if (boton) boton.disabled = false;
}

/**
 * Prompts the user for confirmation to delete the database and sends a DELETE request to the server.
 * 
 * This function displays a confirmation dialog asking the user whether they are sure they want to delete the 
 * information in the database. If the user confirms, it sends a DELETE request to the server using the `fetch` API 
 * with the `Authorization` header set to a bearer token stored in the local storage. 
 * The server response, containing a message, is displayed via an alert.
 * 
 * The function does not take any parameters and will only proceed with the request if the user confirms the action.
 * 
 * @function
 * 
 * @returns {void} This function does not return a value, but it triggers a network request to delete the database.
 * 
 * @example
 * deleteDatabase(); // Asks for confirmation and sends a DELETE request if confirmed.
 */


function deleteDatabase() {
    if (confirm("¿Estás seguro que deseas borrar la información de la base de datos?")) {
        const token = localStorage.getItem("access_token");
        fetch(deleteDatabaseUrl, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message)
            })
            .catch(error => console.error("Error:", error));
    }
}

/**
 * Loads form data for the database configuration from the server.
 * 
 * This function sends a GET request to the server to retrieve the database configuration data. 
 * It populates the form fields with the retrieved values, including the host, port, name, timeout, and date.
 * If the request is successful, the form fields are updated with the corresponding data. 
 * If an error occurs during the request or while processing the data, an error message is logged to the console.
 * 
 * @async
 * @function
 * 
 * @returns {void} This function does not return a value. It updates the DOM with the fetched database settings.
 * 
 * @throws {Error} Throws an error if there is an issue with the network request or processing the response.
 * 
 * @example
 * loadFormDataBase(); // Fetches and populates the form with database configuration data.
 */


async function loadFormDataBase() {
    try {
        const response = await fetch(getFormDataBase);
        if (!response.ok) {
            if (response.status === 401){
                localStorage.removeItem('access_token');
                window.location.href = "{% url 'index' %}"; 

            }
            alert("Error cargando configuraciones de database");
        }
        const data = await response.json();


        const send_average_measure = document.querySelector(`input[name="average_measure"][value="${data.avegare}"]`);
        if (send_average_measure) {
            send_average_measure.checked = true;
        }

        document.getElementById("host").value = data.host;
        document.getElementById("port").value = data.port;
        document.getElementById("name").value = data.name;
        document.getElementById("timeout").value = data.timeout;
        document.getElementById("date").value = data.date;

    } catch (error) {
        // console.error("Error:", error);
    }
}
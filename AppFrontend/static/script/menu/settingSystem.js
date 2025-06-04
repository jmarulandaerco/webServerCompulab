/**
 * Handles the click event for a button and performs actions based on the button ID.
 * 
 * This function changes the visibility or performs specific actions based on the `buttonId` passed as an argument.
 * - If `buttonId` is 1, it calls the `modemManager` function with `false` as an argument.
 * - If `buttonId` is 2, it calls the `deleteWhiteList` function.
 * - If `buttonId` is 3, it calls the `modemManager` function with `true` as an argument.
 * 
 * The purpose of this function is to manage the behavior of different buttons on the UI
 * by triggering appropriate actions when clicked.
 * 
 * @function
 * @param {number} buttonId - The ID of the button that was clicked (1, 2, or 3).
 * 
 * @returns {void} This function doesn't return any value. It triggers specific actions 
 *                 based on the `buttonId`.
 * 
 * @example
 * handleButtonClick(1); // Will call modemManager(false)
 * handleButtonClick(2); // Will call deleteWhiteList()
 * handleButtonClick(3); // Will call modemManager(true)
 */

function handleButtonClick(buttonId) {
    // Dependiendo del botón presionado, cambia la visibilidad de los otros botones

    modemManager(false)
    deleteWhiteList()


}




/**
 * Manages the starting and stopping of the ModemManager service based on the provided flag.
 * 
 * This asynchronous function sends a POST request to a specified service endpoint to start or stop 
 * the ModemManager service. It also updates the UI by showing appropriate buttons and displaying 
 * success or error alerts based on the response.
 * 
 * - If `startManagerModemService` is `true`, the function attempts to start the ModemManager service.
 * - If `startManagerModemService` is `false`, the function attempts to stop the ModemManager service.
 * 
 * It provides feedback to the user with an alert message depending on the success or failure of the 
 * operation. Additionally, the visibility of buttons is updated accordingly.
 * 
 * @async
 * @function
 * @param {boolean} startManagerModemService - A flag indicating whether to start or stop the ModemManager service.
 *   - `true` to start the service.
 *   - `false` to stop the service.
 * 
 * @returns {Promise<void>} This function doesn't return a value but modifies the UI and shows alerts.
 * 
 * @example
 * modemManager(true); // Will attempt to start the ModemManager service.
 * modemManager(false); // Will attempt to stop the ModemManager service.
 */


async function modemManager(startManagerModemService) {
    const response = await fetch(modemManagerService, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ startManagerModemService })


    });

    const data = await response.json();
    if (!response.ok) {
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            window.location.href = "{% url 'index' %}";

        }
        if (startManagerModemService) {
            alert(`❌ Fallo al iniciar el ModemManager.service: ${data.message}`)
        } else {
            alert(`❌ Fallo al parar ModemManager.service ${data.message} `)

        }
    } else {
        if (startManagerModemService) {
            alert("✅ Modem inicio correctamente")

        } else {

            alert("✅ Modem paro correctamente")

        }
    }
}

/**
 * Deletes the whitelist for a selected modem and provides feedback to the user.
 * 
 * This asynchronous function triggers a request to remove the whitelist for a specific modem. 
 * It first prompts the user for confirmation before sending a POST request to a server endpoint. 
 * Based on the server's response, the function either shows a success or error alert, updates the 
 * visibility of UI buttons, and displays additional instructions if successful.
 * 
 * @async
 * @function
 * @returns {Promise<void>} This function doesn't return a value but modifies the UI and shows alerts.
 * 
 * @example
 * deleteWhiteList(); // Prompts user to confirm deletion of the whitelist and processes the result.
 */

async function deleteWhiteList() {
    if (confirm("¿Estás seguro que quieres borrar la whitelists?")) {
        const token = localStorage.getItem("access_token");

        var modemSelect = document.getElementById("modem").value;
        const response = await fetch(viewList, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ modemSelect })

        });
        //La data traera el mensaje que usare en los alert
        const data = await response.json();
        if (!response.ok) {
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                window.location.href = "{% url 'index' %}";

            }
            alert(`❌ Fallo al limpiar la whitelists: ${data.message}`)
        } else {
            alert(`✅ Whitelist limpiada correctamente: ${data.message}`)

            alert(`✅ Recuerda desactivar la simcard de Onomondo, seleccionar el operador de internet yvolver a activar`)
            modemManager(true)
        }
    }
}

/**
 * Configures the Ethernet interface by sending the IP and gateway values to the server.
 * 
 * This asynchronous function collects the IP address and gateway values from the form inputs, 
 * sends them to the server via a POST request for configuring the Ethernet interface, 
 * and displays an alert based on the server's response.
 * 
 * @async
 * @function
 * @returns {Promise<void>} This function doesn't return any value but interacts with the UI by showing alerts.
 * 
 * @example
 * interfaceEthernetOne(); // Sends the IP and gateway values to configure the Ethernet interface.
 */

async function interfaceEthernetOne() {
    const ip = document.getElementById("ipOne").value;
    const gateway = document.getElementById("gatewayOne").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(getInterfaceConnectionOne, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ ip, gateway })
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401) {
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
 * Configures the Ethernet 2 interface by sending the IP and gateway values to the server.
 * 
 * This asynchronous function collects the IP address and gateway values from the form inputs, 
 * sends them to the server via a POST request for configuring the Ethernet interface, 
 * and displays an alert based on the server's response.
 * 
 * @async
 * @function
 * @returns {Promise<void>} This function doesn't return any value but interacts with the UI by showing alerts.
 * 
 * @example
 * interfaceEthernetOne(); // Sends the IP and gateway values to configure the Ethernet interface.
 */
async function interfaceEthernetTwo() {
    const ip = document.getElementById("ipTwo").value;
    const gateway = document.getElementById("gatewayTwo").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    try {
        const response = await fetch(getInterfaceConnectionTwo, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ ip, gateway })
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401) {
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
 * Adds a new WiFi configuration by sending the SSID, password, and name to the server.
 * 
 * This asynchronous function collects the SSID, password, and name values from the form inputs, 
 * sends them to the server via a POST request to add a WiFi configuration, 
 * and displays an alert based on the server's response.
 * 
 * @async
 * @function
 * @returns {Promise<void>} This function doesn't return any value but interacts with the UI by showing alerts.
 * 
 * @example
 * addWifi(); // Sends the SSID, password, and name values to configure a new WiFi network.
 */
async function addWifi() {
    const ssid = document.getElementById("ssid").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(postAddWifi, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ ssid, password, name })
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401) {
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
 * Sends a request to the server to manage the WiFi antenna configuration.
 * 
 * This asynchronous function sends a GET request with an authorization token to the server to 
 * interact with the WiFi antenna configuration. It processes the server's response and displays 
 * an appropriate alert message based on the result.
 * 
 * @async
 * @function
 * @returns {Promise<void>} This function doesn't return any value but interacts with the UI 
 * by showing success or error alerts based on the response from the server.
 * 
 * @example
 * antennaWifi(); // Sends a GET request to manage the WiFi antenna configuration and displays an alert.
 */


async function antennaWifi() {

    try {
        const response = await fetch(postAntennaWifi, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (!response.ok) {
            if (response.status === 401) {
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
 * Fetches and displays the modem information.
 * 
 * This function sends a GET request to the server to retrieve modem information. It includes an
 * authorization token in the request header for authentication. Upon receiving the response,
 * it displays an alert with the result message from the server.
 * 
 * @function
 * @returns {void} This function doesn't return any value, but shows an alert with the response message.
 * 
 * @example
 * showModems(); // Fetches modem information and alerts the user with the server's response message.
 */

function showModems() {

    const token = localStorage.getItem("access_token");
    device_type = document.getElementById("device_type").value
    console.log(device_type)
    fetch(modem, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ device_type })
    })
        .then(response => response.json())
        .then(data => {


            alert("✅ " + data.message)

        })
        .catch(error => { alert("❌" + "Error: "+ error); });
}


async function getIPInterface(interfaceName) {
    try {
        const response = await fetch(`/api/ip/${interfaceName}/`);
        const data = await response.json();

        if (response.ok) {

            if (interfaceName == "eth0") {
                document.getElementById("ipOne").value = data.ip;
                document.getElementById("gatewayOne").value = data.gateway;
                return null
            }

            if (interfaceName == "eth1") {
                document.getElementById("ipTwo").value = data.ip;
                document.getElementById("gatewayTwo").value = data.gateway;
                return null
            }



        } else {
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                window.location.href = "{% url 'index' %}";

            }
            alert("❌ " + `Error: ${data.message}`);

        }
    } catch (error) {
        alert("❌ " + error);

    }
}

function toggleFields() {
    const serverValue = document.getElementById("server").value;

    const neuPlus = document.getElementById("neu_plus").parentElement;
    const telemetry = document.getElementById("telemetry").parentElement;
    const mqtt = document.getElementById("mqtt").parentElement;
    const storage = document.getElementById("storage").parentElement;

    // Ocultar todo
    neuPlus.style.display = "none";
    telemetry.style.display = "none";
    mqtt.style.display = "none";
    storage.style.display = "none";

    console.log(serverValue)
    if (serverValue === "telemetry") {
        neuPlus.style.display = "none";
        mqtt.style.display = "none";
        storage.style.display = "none";

        telemetry.style.display = "block";
    } else if (serverValue === "neu_plus") {
        neuPlus.style.display = "block";
        storage.style.display = "block";
        mqtt.style.display = "block";
        telemetry.style.display = "none";


    } else if (serverValue === "all_services") {
        neuPlus.style.display = "block";
        telemetry.style.display = "block";
        mqtt.style.display = "block";
        storage.style.display = "block";
    }
}

//   method: "POST",
//             headers: {
//                 "Content-Type": "application/json",
//                 "X-CSRFToken": csrfToken
//             },
//             body: JSON.stringify({ ssid, password, name })
function WLan() {
    device_type = document.getElementById("device_type_wlan").value

    fetch(wlan, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body:JSON.stringify({device_type})
    })
        .then(response => response.json())
        .then(data => {
            if (data.ok) {

                alert(data.message)
            } else {
                alert(data.message)
            }
        })
        .catch(error => {
            alert("❌ " + 'Error al verificar la ip:', error);
        });
}

async function addPLC() {
    const interface = document.getElementById("plc").value;
    const ip = document.getElementById("plcIp").value;
    const port = document.getElementById("port_device").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;


    try {
        const response = await fetch(plc, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken

            },
            body: JSON.stringify({ interface, ip, port })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error, comando no aplicado " + data.message);

        } else {
            alert("✅ " + data.message);
            const minutes = 360;
            const delay = minutes * 60 * 1000;

            setTimeout(() => {
                deletePLC(interface, ip, port);
               

            }, delay);


        }

    } catch (error) {
        alert("❌ " + error.message);
        // console.error("Error:", error);
    }
};


async function deletePLC(interfaceEntry = null, ipEntry = null, portEntry = null) {
    let interfaceValue, ip, port;

    if (interfaceEntry === null) {
        interfaceValue = document.getElementById("plc").value;
    } else {
        interfaceValue = interfaceEntry;
    }

    if (ipEntry === null) {
        ip = document.getElementById("plcIp").value;
    } else {
        ip = ipEntry;
    }

    if (portEntry === null) {
        port = document.getElementById("port_device").value;
    } else {
        port = portEntry;
    }

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(plc, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ interface: interfaceValue, ip, port })
        });

        const data = await response.json();

        if (!response.ok) {
            if (interfaceEntry === null) {
                alert("❌ " + "Error, comando no aplicado " + data.message);
            }
        } else {
            if (interfaceEntry === null) {
                alert("✅ " + data.message);
            }

        }

    } catch (error) {
        alert("❌ " + error.message);
    }
}

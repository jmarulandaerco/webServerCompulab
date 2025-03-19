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
    if (buttonId === 2) {
        modemManager(false)
        deleteWhiteList()
        
    } 
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
    console.log
    const response = await fetch(modemManagerService,{
        method:"POST",
        headers:{
            "Authorization": `Bearer ${token}`,  
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ startManagerModemService })


    });

    const data = await response.json();
    if(!response.ok){

        if(startManagerModemService){
            alert(`❌ failure to start ModemManager.service: ${data.message}`)
        }else{
            alert(`❌ failure to stop ModemManager.service ${data.message} `)

        }
    }else{
        if(startManagerModemService){
            alert("✅ Modem started correctly")
          
        }else{
            
            alert("✅ Modem stopped correctly")

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
    if(confirm("¿Are you sure you want to delete the whiteList?")){
        const token = localStorage.getItem("access_token"); 

        var modemSelect = document.getElementById("modem").value;
        console.log(modemSelect)
        const response =await fetch(viewList, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,  
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ modemSelect })

        });
        //La data traera el mensaje que usare en los alert
        const data = await response.json();
        if (!response.ok){
            alert(`❌ Failed to clear the whitelist: ${data.message}`)
        }else{
            alert(`✅ Whitelist successfully cleared: ${data.message}`)
          
            alert(`✅ Remember to deactivate your onomondo simcar, edit and select your internet operator, re-activate it, and you can start your modem. `)
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
    const ip = document.getElementById("ip").value;
    const gateway = document.getElementById("gateway").value;
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

            alert("❌ " + "Validation error");
            
        } else {
            alert("✅ " + data.message);
            

        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
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
    const ip = document.getElementById("ip").value;
    const gateway = document.getElementById("gateway").value;
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

            alert("❌ " + "Validation error");

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
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

            alert("❌ " + "Validation error");

        } else {
            alert("✅ " + data.message);

        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
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

            alert("❌ " + "Validation error");

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
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

    fetch(modem, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {


            alert(data.message)

        })
        .catch(error => { console.error("Error:", error); });
}

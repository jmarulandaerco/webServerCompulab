/**
 * Updates modem checker settings by sending a PUT request with the provided connection and attempt data.
 * 
 * This function gathers the values for `connection` and `attemts` from the DOM and sends them to the server 
 * via a PUT request to update the modem checker settings. The request includes a CSRF token for security.
 * The function then handles the server response, showing appropriate success or error messages.
 * 
 * @async
 * @function
 * @param {void} 
 * 
 * @returns {void} This function does not return any value but alerts the user with the outcome of the operation.
 * 
 * @throws {Error} If the fetch operation fails or the response is not OK, the function alerts the user with the error message.
 * 
 * @example
 * updateModemChecker(); // Sends modem checker settings to the server and updates the UI based on the response.
 */

async function updateModemChecker() {
    const connection = document.getElementById("connection").value;
    const attemts = document.getElementById("attemts").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 
    try {
        const response =  await fetch(getFormDataModemChecker, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ connection, attemts })
        });

        const data =  await response.json();

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
 * Updates modem signal settings by sending a PUT request with the provided onomondo and minimum signal data.
 * 
 * This function collects the values of `onomondo` and `minimum` from the DOM and sends them to the server
 * via a PUT request to update the modem signal settings. The request includes a CSRF token for security.
 * The function then handles the server response, showing appropriate success or error messages.
 * 
 * @async
 * @function
 * @param {void} 
 * 
 * @returns {void} This function does not return any value but alerts the user with the outcome of the operation.
 * 
 * @throws {Error} If the fetch operation fails or the response is not OK, the function alerts the user with the error message.
 * 
 * @example
 * updateModemSignal(); // Sends modem signal settings to the server and updates the UI based on the response.
 */

async function updateModemSignal() {
    const onomondo = document.getElementById("onomondo").value;
    const minimum = document.getElementById("minimum").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        const response =  await fetch(getFormDataSignalChecker, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ onomondo, minimum })
        });

        const data =  await response.json();

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
 * Updates server request settings by sending a PUT request with the provided request count data.
 * 
 * This function collects the `requests` value from the DOM and sends it to the server
 * via a PUT request to update the server request settings. The request includes a CSRF token for security.
 * After the request is sent, the function handles the server response, showing appropriate success or error messages.
 * 
 * @async
 * @function
 * @param {void} 
 * 
 * @returns {void} This function does not return any value but alerts the user with the outcome of the operation.
 * 
 * @throws {Error} If the fetch operation fails or the response is not OK, the function alerts the user with the error message.
 * 
 * @example
 * updateModemServer(); // Sends server request settings to the server and updates the UI based on the response.
 */

async function updateModemServer() {
    const requests = document.getElementById("requests").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        const response =  await fetch(getFormDataServerChecker, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ requests })
        });

        const data =  await response.json();

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

async function updateAwsSettings(){
    const client = document.getElementById("clientId").value;
    const certicate = document.getElementById("clientCertificate").value;   
    const private = document.getElementById("private").value;   
    try{
        const response = await fetch(elementary,{
            method:"PUT",
           
            body:JSON.stringify({client,certicate,private})
        });

        const data = await response.json();
        if(!response.ok){
            alert("❌ " + "Error in validation"); 
        }else{
            alert("✅ " + data.message);
        }
    }catch(error){
        alert("❌ " + error.message);
        console.log(error)
    }

}
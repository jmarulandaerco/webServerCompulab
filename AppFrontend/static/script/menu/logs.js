/**
 * Prompts the user for confirmation and deletes logs if confirmed.
 * 
 * This function asks the user for confirmation before sending a `DELETE` request to the server to delete logs. It uses the token stored in the local storage for authentication. If the user confirms the deletion, the request is made to the server. After the request, a success or error message is displayed based on the server's response.
 * 
 * @function
 * @returns {void} This function does not return a value but triggers the deletion process and shows an alert based on the success or failure of the request.
 * 
 * @example
 * deletelog(); // Prompts the user to confirm and deletes the logs if confirmed.
 */

function deletelog() {
    if (confirm("Are you sure to delete logs?")) {
        const token = localStorage.getItem("access_token");

        fetch(deleteLog, {
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
 * Fetches and displays logs from the server.
 * 
 * This function sends an asynchronous request to fetch log data from the server. Upon receiving the data, it displays the logs in a container on the page. If logs are found, they are displayed in reverse order, with each log line wrapped in a `div` element. If no logs are found, a message indicating that no logs are available is displayed.
 * 
 * @async
 * @function
 * @returns {void} This function does not return a value. It modifies the DOM by updating the content of a log container.
 * 
 * @example
 * fetchLogs(); // Fetches logs and displays them in the log container element.
 */

async function fetchLogs() {
    try {
        const response = await fetch(fetchLog);
        const data = await response.json();
        const logContainer = document.getElementById("log-container");



        if (data.logs) {
            logContainer.innerHTML = data.logs
                .reverse()
                .map(line => `<div class="log-line">${line}</div>`)
                .join("");
        } else {
            logContainer.innerText = "No logs found.";
        }
    } catch (error) {
        console.error("Error retrieving logs:", error);
    }
}

/**
 * Downloads logs from the server and triggers a download of the log file.
 * 
 * This function sends an asynchronous request to fetch log data from the server. The data is received as a binary `blob` and converted into a downloadable file. The file is then automatically downloaded by the user, with the file named `logs.zip`. If the request fails or an error occurs, an error message is logged to the console, and a user-friendly alert is shown.
 * 
 * @async
 * @function
 * @returns {void} This function does not return any value. It triggers a file download in the browser.
 * 
 * @throws {Error} If there is an issue with fetching the logs, an error is thrown and handled in the catch block.
 * 
 * @example
 * downloadLogs(); // Initiates the process of downloading the logs as a zip file.
 */

async function downloadLogs() {
    try {
        const response = await fetch(downloadLog); // Reemplaza con la URL real

        if (!response.ok) {
            throw new Error("Failed to fetch logs");
        }

        const blob = await response.blob(); // Convertir la respuesta en un blob
        const url = window.URL.createObjectURL(blob);

        // Crear un enlace para descargar el archivo
        const a = document.createElement("a");
        a.href = url;
        a.download = "logs.zip"; // Nombre del archivo a descargar
        document.body.appendChild(a);
        a.click();

        // Limpiar
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error("Error downloading logs:", error);
        alert("Error downloading logs. Please try again.");
    }
}


async function getLogSingleDevice() {
    try {
        document.querySelector('.container_logs').style.display = 'block';

        const response = await fetch(fetchSingleDevice);
        const data = await response.json();
        const logContainer = document.getElementById("content4");



        if (data.logs) {
            logContainer.innerHTML = data.logs
                .reverse()
                .map(line => `<div class="log-line">${line}</div>`)
                .join("");
        } else {
            logContainer.innerText = "No logs found.";
        }
    } catch (error) {
        console.error("Error retrieving logs:", error);
    }
}
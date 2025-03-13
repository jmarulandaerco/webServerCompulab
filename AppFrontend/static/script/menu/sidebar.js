
/**
 * Downloads a collection of data as a text file. The function fetches the collection from the server,
 * generates a filename with the current date and time, and prompts the user to download the file.
 * 
 * The filename follows the format `collections_YYYYMMDDHHMMSS.txt`, where the date and time are based
 * on the moment the function is invoked. The file contains the collection data retrieved from the server
 * as a blob.
 * 
 * This function performs the following:
 * - Retrieves the collection data from the server by sending a fetch request.
 * - Converts the response into a blob to allow file download.
 * - Generates a downloadable link with the blob and triggers the download using an anchor (`<a>`) element.
 * - The generated file is named with the current timestamp to ensure uniqueness.
 * 
 * @function
 * @returns {void} This function doesn't return anything, it triggers the download of the collection data as a file.
 * 
 * @example
 * downloadCollections();
 */

function downloadCollections() {
    const now = new Date();
    const dateString = now.toISOString().replace(/[-:.]/g, ''); // Formato 'YYYYMMDDHHMMSS'
    const filename = `collections_${dateString}.txt`;

    fetch(listCollection)
        .then(response => {
            if (!response.ok) {
                alert("Error while downloading");
            }
            return response.blob(); 
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = filename; // Usar el nombre del archivo con la fecha y hora
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error("Error:", error));
}

/**
 * Prompts the user to confirm if they want to restart the Erco Pulse device.
 * If confirmed, sends a GET request to the server to reboot the device. 
 * The function uses an access token stored in the localStorage for authorization.
 * 
 * The request is sent to the `reboot` endpoint with an Authorization header 
 * containing the Bearer token for authentication. After the request is completed,
 * it displays an alert with the server's response message. If an error occurs,
 * it is logged to the console.
 * 
 * @function
 * @returns {void} This function doesn't return anything. It triggers a confirmation prompt
 *                 and sends a request to reboot the device if confirmed.
 * 
 * @example
 * rebootErcoPulse();
 */

function rebootErcoPulse() {
    if (confirm("Are you sure about restarting the Erco Pulse?")) {
        const token = localStorage.getItem("access_token"); 

        fetch(reboot, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,  
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message); 
            })
            .catch(error => console.error("Error:", error));
    }
}




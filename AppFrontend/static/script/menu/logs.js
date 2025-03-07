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
async function fetchLogs() {
    try {
        const response = await fetch(fetchLog);
        const data = await response.json();
        const logContainer = document.getElementById("log-container");



        if (data.logs) {
            logContainer.innerHTML = data.logs
                .map(line => `<div class="log-line">${line}</div>`)
                .join("");
        } else {
            logContainer.innerText = "No logs found.";
        }
    } catch (error) {
        console.error("Error retrieving logs:", error);
    }
}

async function downloadLogs() {
    try {
        const response = await fetch("downloadLog"); // Reemplaza con la URL real

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
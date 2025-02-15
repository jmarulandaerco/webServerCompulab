function deletelog() {
    if (confirm("¿Estás seguro de borrar los logs?")) {
        const token = localStorage.getItem("access_token"); // Obtiene el token del localStorage

        fetch(deleteLog, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`,  // Enviar token en la cabecera
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
            logContainer.innerText = "No se encontraron logs.";
        }
    } catch (error) {
        console.error("Error obteniendo los logs:", error);
    }
}
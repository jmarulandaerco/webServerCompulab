function deleteDatabase() {
    if (confirm("¿Estás seguro de borrar la información en la Base de datos?")) {
        const token = localStorage.getItem("access_token"); // Obtiene el token del localStorage

        fetch(deleteDatabaseUrl, {
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
function downloadCollections() {
    fetch(listCollection)
        .then(response => {
            if (!response.ok) {
                throw new Error("Error en la descarga");
            }
            return response.blob(); // Convertimos la respuesta en un Blob
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "colecciones.txt"; // Nombre del archivo
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error("Error:", error));
}
function rebootErcoPulse() {
    if (confirm("¿Estás seguro de reinir el Erco Pulse")) {
        const token = localStorage.getItem("access_token"); // Obtiene el token del localStorage

        fetch(reboot, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,  // Enviar token en la cabecera
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                alert(data.message); // Muestra el mensaje de respuesta
            })
            .catch(error => console.error("Error:", error));
    }
}




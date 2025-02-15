function checkServiceStatus() {
    fetch(statusService)  // Ajusta esto con la URL real de tu API
        .then(response => response.json())
        .then(data => {
            const statusCircle = document.getElementById('statusCircle');
            const statusText = document.getElementById('statusText');
            console.log("Hecho")
            if (data.active) {
                statusCircle.classList.remove('inactive');
                statusCircle.classList.add('active');
                statusText.innerText = 'Activo';
            } else {
                statusCircle.classList.remove('active');
                statusCircle.classList.add('inactive');
                statusText.innerText = 'Inactivo';
            }
        })
        .catch(error => console.error('Error al obtener el estado:', error));
}
function startService() {
    if (confirm("¿Estás seguro de iniciar el servicio?")) {
        const token = localStorage.getItem("access_token"); // Obtiene el token del localStorage

        fetch(start, {
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

                if (data.message == "Reiniciando sistema, espera 30 segundos  por favor") {
                    setTimeout(() => {
                        checkServiceStatus(); // Ejecuta la función después de 5 segundos
                    }, 20000);
                }

            })
            .catch(error => console.error("Error:", error));
    }
}
function stopService() {
    if (confirm("¿Estás seguro de parar el servicio?")) {
        const token = localStorage.getItem("access_token"); // Obtiene el token del localStorage

        fetch(stop, {
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

                if (data.message == "Parando Sistema") {
                    setTimeout(() => {
                        checkServiceStatus(); // Ejecuta la función después de 5 segundos
                    }, 2000);
                }
            })
            .catch(error => console.error("Error:", error));
    }
}
function checkServiceStatus() {
    fetch(statusService)  
        .then(response => response.json())
        .then(data => {
            const statusCircle = document.getElementById('statusCircle');
            const statusText = document.getElementById('statusText');
            console.log("Hecho")
            console.log(data.active)
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
    if (confirm("¿Estás seguro de iniciar el servicio?, este tardara 30 segundos en iniciar")) {
        const token = localStorage.getItem("access_token"); 

        fetch(start, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,  
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json())
            .then(data => {



                alert(data.message);
                checkServiceStatus();

            })
            .catch(error => console.error("Error:", error));
    }
}
function stopService() {
    if (confirm("¿Estás seguro de parar el servicio?")) {
        const token = localStorage.getItem("access_token"); 

        fetch(stop, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`, 
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json())
            .then(data => {
                console.log(data)
                alert(data.message);

                if (data.message == "Parando Sistema") {
                    setTimeout(() => {
                        checkServiceStatus(); 
                    }, 2000);
                }
            })
            .catch(error => console.error("Error:", error));
    }
}
function checkServiceStatus() {
    fetch(statusService)  
        .then(response => response.json())
        .then(data => {
            const statusCircle = document.getElementById('statusCircle');
            const statusText = document.getElementById('statusText');

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
        .catch(error => console.error('Error when obtaining the status:', error));
}
function startService() {
    if (confirm("Are you sure you want to start the service?, it will take 30 seconds to start.")) {
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
    if (confirm("Are you sure to stop the service?")) {
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
                alert(data.message);

                if (!response.ok) {
                    setTimeout(() => {
                        checkServiceStatus(); 
                    }, 2000);
                }
            })
            .catch(error => console.error("Error:", error));
    }
}
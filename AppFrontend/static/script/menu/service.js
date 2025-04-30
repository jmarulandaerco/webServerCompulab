/**
 * Checks the status of a service and updates the UI to reflect whether it is active or inactive.
 * 
 * This function sends a GET request to the server to retrieve the status of a service. Based on the response,
 * it updates the visual indicators (status circle and text) to show if the service is active or inactive.
 * 
 * - If the service is active, the status circle turns green and the text is updated to "Activo".
 * - If the service is inactive, the status circle turns red and the text is updated to "Inactivo".
 * 
 * @function
 * @returns {void} This function doesn't return any value, but it updates the DOM elements related to the service status.
 * 
 * @example
 * checkServiceStatus(); // Checks the service status and updates the status circle and text.
 */

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
        .catch(error =>{
            
        });

}

/**
 * Starts a service and displays progress feedback during the startup.
 * 
 * This function prompts the user for confirmation to start a service. If the user confirms, it triggers a progress bar
 * to indicate the service startup process, which takes about 30 seconds. After the service has started, the function
 * checks the status of the service and updates the UI accordingly.
 * 
 * The function sends a GET request to start the service and includes an authorization token for authentication.
 * After starting the service, the function waits for a response, displays an alert with the message from the server,
 * and then checks the service status after a brief delay.
 * 
 * @function
 * @returns {void} This function doesn't return any value but triggers UI changes (progress bar, alerts).
 * 
 * @example
 * startService(); // Starts the service and updates the UI with the progress and status.
 */

function startService() {
    const boton = document.getElementById("startServiceButton");
    boton.disabled = true;
    if (confirm("¿Estás seguro de iniciar el servicio? Tomará 30 segundos en iniciar")) {
        const token = localStorage.getItem("access_token");
        startProgressBar();
        fetch(start, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        })
            .then(response => response.json())
            .then(data => {



                setTimeout(function () {
                    checkServiceStatus();
                    alert(data.message);
                }, 30000);


            })
            .catch(error => {
                
            })
            .finally(() => {
                checkServiceStatus();
                boton.disabled = false
            });
    } else {
        boton.disabled = false
    }
}

/**
 * Starts a service and displays progress feedback during the startup.
 * 
 * This function prompts the user for confirmation to start a service. If the user confirms, it triggers a progress bar
 * to indicate the service startup process, which takes about 30 seconds. After the service has started, the function
 * checks the status of the service and updates the UI accordingly.
 * 
 * The function sends a GET request to start the service and includes an authorization token for authentication.
 * After starting the service, the function waits for a response, displays an alert with the message from the server,
 * and then checks the service status after a brief delay.
 * 
 * @function
 * @returns {void} This function doesn't return any value but triggers UI changes (progress bar, alerts).
 * 
 * @example
 * startService(); // Starts the service and updates the UI with the progress and status.
 */

function stopService() {
    const boton = document.getElementById("stopServiceButton");
    boton.disabled = true;
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
                alert(data.message);


                setTimeout(() => {
                    checkServiceStatus();
                }, 1000);

            })
            .catch(error => {
                
            }).finally(() => {
                boton.disabled = false;

            });
    } else {
        boton.disabled = false;

    }
}


/**
 * Starts a progress bar that visually indicates the passage of time over 30 seconds.
 * 
 * This function displays a progress bar and animates its width from 0% to 100% over a duration of 30 seconds.
 * The progress bar's container is shown, and the bar's width is updated in real time based on the elapsed time.
 * Once the progress reaches 100%, the progress bar container is hidden after a brief delay.
 * 
 * @function
 * @returns {void} This function does not return any value but visually updates the progress bar's display.
 * 
 * @example
 * startProgressBar(); // Starts the progress bar animation and shows the status over 30 seconds.
 */

function startProgressBar() {
    let progressBar = document.getElementById("progressBar");
    let progressContainer = document.getElementById("progressBarContainer");

    progressContainer.style.display = "block"; // Mostrar la barra
    progressBar.style.width = "0%"; // Resetear

    let startTime = Date.now();
    let duration = 31000; // 5 segundos

    function updateProgress() {
        let elapsedTime = Date.now() - startTime;
        let percentage = (elapsedTime / duration) * 100;

        progressBar.style.width = percentage + "%";

        if (percentage < 100) {
            requestAnimationFrame(updateProgress);
        } else {
            setTimeout(() => {
                progressContainer.style.display = "none";
            }, 500);
        }
    }

    requestAnimationFrame(updateProgress);
    checkServiceStatus()
}
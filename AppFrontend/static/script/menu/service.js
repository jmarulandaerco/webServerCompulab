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
        .catch(error => console.error('Error when obtaining the status:', error));
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
    if (confirm("Are you sure you want to start the service?, it will take 30 seconds to start.")) {
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

                console.log(data)

                
                setTimeout(function() {
                    checkServiceStatus();
                },30000);
                alert(data.message);

            })
            .catch(error => console.error("Error:", error));
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

                
                    setTimeout(() => {
                        checkServiceStatus(); 
                    }, 2000);
                
            })
            .catch(error => console.error("Error:", error));
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
    let duration = 30000; // 30 segundos

    function updateProgress() {
        let elapsedTime = Date.now() - startTime;
        let percentage = (elapsedTime / duration) * 100;

        progressBar.style.width = percentage + "%";

        if (percentage < 100) {
            requestAnimationFrame(updateProgress);
        }else {
            setTimeout(() => {
                progressContainer.style.display = "none";
            }, 500); 
        }
    }

    requestAnimationFrame(updateProgress);
}
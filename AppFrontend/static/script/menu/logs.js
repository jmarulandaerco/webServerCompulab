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
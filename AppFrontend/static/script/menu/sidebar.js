function deleteDatabase() {
    if (confirm("Are you sure you want to delete the information in the database?")) {
        const token = localStorage.getItem("access_token"); 

        fetch(deleteDatabaseUrl, {
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
function downloadCollections() {
    fetch(listCollection)
        .then(response => {
            if (!response.ok) {
                alert.error("Error while downloading");
            }
            return response.blob(); 
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "colecciones.txt"; 
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error("Error:", error));
}
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




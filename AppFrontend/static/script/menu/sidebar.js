
function downloadCollections() {
    const now = new Date();
    const dateString = now.toISOString().replace(/[-:.]/g, ''); // Formato 'YYYYMMDDHHMMSS'
    const filename = `collections_${dateString}.txt`;

    fetch(listCollection)
        .then(response => {
            if (!response.ok) {
                alert("Error while downloading");
            }
            return response.blob(); 
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = filename; // Usar el nombre del archivo con la fecha y hora
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




async function updateInformationDatabase() {
    const host = document.getElementById("host").value;
    const port = document.getElementById("port").value;
    const name = document.getElementById("name").value;
    const timeout = document.getElementById("timeout").value;
    const date = document.getElementById("date").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 
    try {
        const response =  await fetch(getFormDataBase, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ host,port,name,timeout,date })
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation"); 

        } else {
            alert("✅ " + data.message); 
             

        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};

async function loadFormDataSettingDatabase() {
    try {
        const response = await fetch(getFormDataUrlSettingDatabase);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();
        document.getElementById("day").value = data.day;
        document.getElementById("awaitTime").value = data.awaitTime;
    } catch (error) {
        console.error("Error:", error);
    }
}

async function updateSettingDatabase() {
    const day = document.getElementById("day").value;
    const awaitTime = document.getElementById("awaitTime").value;
   

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        const response =  await fetch(getFormDataUrlSettingDatabase, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ day,awaitTime })
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation"); 

        } else {
            alert("✅ " + data.message); 
             

        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};

function exportToExcel() {
    const url = '/api/inverter/export/';
    const a = document.createElement('a');
    const dateString = now.toISOString().replace(/[-:.]/g, ''); // Formato 'YYYYMMDDHHMMSS'
    const filename = `investor_data${dateString}.txt`;
    a.href = url;
    a.download = `${filename}.xlsx`; 
    a.click();
}



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

async function loadFormDataBase() {
    try {
        const response = await fetch(getFormDataBase);
        if (!response.ok) {
            throw new Error("Error in loading the data");
        }
            const data = await response.json();

            document.getElementById("host").value = data.host;
            document.getElementById("port").value = data.port;
            document.getElementById("name").value = data.name;
            document.getElementById("timeout").value = data.timeout;
            document.getElementById("date").value = data.date;
            
    } catch (error) {
        console.error("Error:", error);
    }
}
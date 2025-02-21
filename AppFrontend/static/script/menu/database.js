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
            alert.error("Error loading data");
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
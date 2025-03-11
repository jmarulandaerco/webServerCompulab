async function deleteWhiteList() {
    if(confirm("¿Are you sure you want to delete the whiteList?")){
        const token = localStorage.getItem("access_token"); 

        const response =await fetch(deleteDatabaseUrl, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`,  
                "Content-Type": "application/json"
            }
        });
        //La data traera el mensaje que usare en los alert
        const data = await response.json();
        if (!response.ok){
            alert("❌ Failed to clear the whitelist")
        }else{
            alert("✅ whitelist successfully cleared")
        }
    }
}

async function interfaceEthernetOne() {
    const ip = document.getElementById("ip").value;
    const gateway = document.getElementById("gateway").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(getInterfaceConnectionOne, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ ip, gateway })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Validation error");

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
    }
};
async function interfaceEthernetTwo() {
    const ip = document.getElementById("ip").value;
    const gateway = document.getElementById("gateway").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    try {
        const response = await fetch(getInterfaceConnectionTwo, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ ip, gateway })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Validation error");

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
    }
};
async function addWifi() {
    const ssid = document.getElementById("ssid").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(postAddWifi, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ ssid, password, name })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Validation error");

        } else {
            alert("✅ " + data.message);

        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
    }
};
async function antennaWifi() {

    try {
        const response = await fetch(postAntennaWifi, {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Validation error");

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
    }
};
function showModems() {

    const token = localStorage.getItem("access_token");

    fetch(modem, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json"
        }
    })
        .then(response => response.json())
        .then(data => {


            alert(data.message)

        })
        .catch(error => { console.error("Error:", error); });
}

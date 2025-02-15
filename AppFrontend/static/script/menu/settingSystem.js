async function interfaceEthernetOne() {
    const ip = document.getElementById("ip").value;
    const gateway = document.getElementById("gateway").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        const response =  await fetch(getInterfaceConnectionOne, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ ip, gateway })
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error en la validación"); // Muestra éxito si las contraseñas coinciden

        } else {
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden
             

        }

    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};
async function interfaceEthernetTwo() {
    const ip = document.getElementById("ip").value;
    const gateway = document.getElementById("gateway").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        const response =  await fetch(getInterfaceConnectionTwo, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ ip, gateway })
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error en la validación"); // Muestra éxito si las contraseñas coinciden

        } else {
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden
             

        }

    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};
async function addWifi() {
    const ssid = document.getElementById("ssid").value;
    const password = document.getElementById("password").value;
    const name = document.getElementById("name").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        const response =  await fetch(postAddWifi, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ ssid, password,name })
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error en la validación"); // Muestra éxito si las contraseñas coinciden

        } else {
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden
             

        }

    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};
async function antennaWifi() {
    
    try {
        const response =  await fetch(postAntennaWifi, {
            method: "GET",
            headers: {
                 "Authorization": `Bearer ${token}`,  // Enviar token en la cabecera
                 "Content-Type": "application/json"
            }
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error en la validación"); // Muestra éxito si las contraseñas coinciden

        } else {
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden
             

        }

    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};
function showModems() {

const token = localStorage.getItem("access_token"); // Obtiene el token del localStorage

fetch(modem, {
method: "GET",
headers: {
    "Authorization": `Bearer ${token}`,  // Enviar token en la cabecera
    "Content-Type": "application/json"
}
})
.then(response => response.json())
.then(data => {


    alert(data.message)

})
.catch(error => { console.error("Error:", error); console.log(response) });
}

async function updateInformationDatabase() {
    const host = document.getElementById("host").value;
    const port = document.getElementById("port").value;
    const name = document.getElementById("name").value;
    const timeout = document.getElementById("timeout").value;
    const date = document.getElementById("date").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        console.log(getFormDataModemChecker)
        const response =  await fetch(getFormDataBase, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ host,port,name,timeout,date })
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

async function loadFormDataSettingDatabase() {
    try {
        const response = await fetch(getFormDataUrlSettingDatabase);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
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
   

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        console.log(getFormDataModemChecker)
        const response =  await fetch(getFormDataUrlSettingDatabase, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ day,awaitTime })
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
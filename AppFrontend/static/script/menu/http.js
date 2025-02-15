async function updateModemChecker() {
    const connection = document.getElementById("connection").value;
    const attemts = document.getElementById("attemts").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        const response =  await fetch(getFormDataModemChecker, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ connection, attemts })
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
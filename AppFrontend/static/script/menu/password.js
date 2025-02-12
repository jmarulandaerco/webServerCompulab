
async function checked() {

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token
    console.log(password)
    console.log(confirmPassword)
    try {
        const response = await fetch(postCheckPasswordUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ password, confirmPassword })
        });

        const data = await response.json();
        console.log("Hola")
        console.log(data)

        if (!response.ok) {
            
            alert("✅ " + data.error); // Muestra éxito si las contraseñas coinciden
            throw new Error(data.error || "Error en la validación");
            

        }else{
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden

        }


    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};

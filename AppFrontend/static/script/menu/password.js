
async function changePassword(){
    const actualPassword = document.getElementById("actualPassword").value;
    const newPassword = document.getElementById("newPassword").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token
    try{
        const response = await fetch(changePasswordUrl, {
            method: "PUT", // Especificar el método PUT
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ actualPassword, newPassword }) 
     });

        const data=await  response.json();
        console.log(data)
        if (!response.ok) {
            
            alert("❌ "  + "Error en la validación"); // Muestra éxito si las contraseñas coinciden

        }else{
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden

        }
    }catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }   
}

async function checked() {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

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
      
        if (!response.ok) {
            
            alert("❌ "  + "Error en la validación"); // Muestra éxito si las contraseñas coinciden

        }else{
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden
            await loadContent('form/database')

        }

    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};


async function checkedPassWordLog() {

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

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
      
        if (!response.ok) {
            
            alert("❌ "  + "Error en la validación"); // Muestra éxito si las contraseñas coinciden
            // await loadContentMenu('settingLog')

        }else{
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden
            await loadContentMenu('settingLog')

        }

    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};



async function loadFormDataBase() {
    try {
        const response = await fetch(getFormDataBase);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
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


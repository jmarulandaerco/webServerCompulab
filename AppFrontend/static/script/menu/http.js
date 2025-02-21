async function updateModemChecker() {
    const connection = document.getElementById("connection").value;
    const attemts = document.getElementById("attemts").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 
    try {
        console.log(getFormDataModemChecker)
        const response =  await fetch(getFormDataModemChecker, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ connection, attemts })
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error en la validación"); 

        } else {
            alert("✅ " + data.message);
             

        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};
async function updateModemSignal() {
    const onomondo = document.getElementById("onomondo").value;
    const minimum = document.getElementById("minimum").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        console.log(getFormDataModemChecker)
        const response =  await fetch(getFormDataSignalChecker, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ onomondo, minimum })
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error en la validación"); 

        } else {
            alert("✅ " + data.message);
             

        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};
async function updateModemServer() {
    const requests = document.getElementById("requests").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        console.log(getFormDataModemChecker)
        const response =  await fetch(getFormDataServerChecker, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ requests })
        });

        const data =  await response.json();

        if (!response.ok) {

            alert("❌ " + "Error en la validación"); 

        } else {
            alert("✅ " + data.message); 
             

        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};
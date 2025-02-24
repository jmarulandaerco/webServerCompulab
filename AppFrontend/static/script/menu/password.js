
async function changePassword(){
    const actualPassword = document.getElementById("actualPassword").value;
    const newPassword = document.getElementById("newPassword").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    try{
        const response = await fetch(changePasswordUrl, {
            method: "PUT", 
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ actualPassword, newPassword }) 
     });

        const data=await  response.json();
        if (!response.ok) {
            
            alert("❌ "  + "Validation error"); 

        }else{
            alert("✅ " + data.message);
        }
    }catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }   
}

async function checked() {
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        const response = await fetch(postCheckPasswordUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ password, confirmPassword })
        });

        const data = await response.json();
      
        if (!response.ok) {
            
            alert("❌ "  + "Validation error"); 

        }else{
            alert("✅ " + data.message); 
            await loadContent('form/database/database')

        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};

async function checkedPassWordLog() {

    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; 

    try {
        const response = await fetch(postCheckPasswordUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken 
            },
            body: JSON.stringify({ password, confirmPassword })
        });

        const data = await response.json();
      
        if (!response.ok) {
            
            alert("❌ "  + "Validation error"); 
            

        }else{
            alert("✅ " + data.message); 
            await loadContentMenu('settingLog')

        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
    }
};

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


const username = localStorage.getItem("username") || "Invitado";
document.getElementById("usernameHeader").textContent = username;
console.log("Culis")
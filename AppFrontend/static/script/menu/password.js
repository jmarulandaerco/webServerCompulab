
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





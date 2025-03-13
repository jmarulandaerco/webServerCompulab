/**
 * Changes the user's password by sending a request to the server with the new password.
 * 
 * This function collects the current and new password values from input fields and sends them to the server for validation and updating.
 * A CSRF token is included to protect against cross-site request forgery attacks. If the request is successful, a confirmation message is displayed.
 * If the request fails, an error message is shown to the user.
 * 
 * @async
 * @function
 * @returns {void} This function does not return a value but displays alerts based on the success or failure of the password change request.
 * 
 * @example
 * changePassword(); // Changes the user's password after receiving input for the current and new passwords.
 */

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

/**
 * Validates and checks if the password and confirmation password match.
 * 
 * This function retrieves the password and confirmation password entered by the user, then sends them to the server for validation. 
 * The request includes a CSRF token for security. If the passwords match and the request is successful, a success message is displayed. 
 * If the passwords do not match or if there is an error with the request, an error message is shown.
 * 
 * @async
 * @function
 * @returns {void} This function does not return a value but displays alerts based on the success or failure of the password validation request.
 * 
 * @example
 * checked(); // Sends the password and confirmPassword to the server for validation.
 */

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
            await loadContent('form/database/databaseSetting')

        }

    } catch (error) {
        alert("❌ " + error.message); 
        console.error("Error:", error);
    }
};


/**
 * Validates the password and confirmation password entered by the user, then triggers a server-side check.
 * 
 * This function retrieves the password and confirmation password entered by the user, and sends them to the server for validation. 
 * It includes a CSRF token for security. If the passwords match and the request is successful, a success message is displayed. 
 * If there is a validation error or the passwords do not match, an error message is shown. Upon success, the content for the "settingLog" section is reloaded.
 * 
 * @async
 * @function
 * @returns {void} This function does not return a value but shows an alert based on the success or failure of the password validation request.
 * 
 * @example
 * checkedPassWordLog(); // Sends the password and confirmPassword to the server for validation and reloads the "settingLog" content.
 */


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





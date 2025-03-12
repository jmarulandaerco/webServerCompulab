function handleButtonClick(buttonId) {
    // Dependiendo del botón presionado, cambia la visibilidad de los otros botones
    if (buttonId === 1) {
        modemManager(false)
       
    } else if (buttonId === 2) {

        deleteWhiteList()
        
    } else if (buttonId === 3) {
        modemManager(true)

    }
}

async function modemManager(startManagerModemService) {
    const response = await fetch(modemManagerService,{
        method:"POST",
        headers:{
            "Authorization": `Bearer ${token}`,  
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ startManagerModemService })


    });

    const data = await response.json();
    if(!response.ok){

        if(startManagerModemService){
            alert(`❌ failure to start ModemManager.service: ${data.message}`)
        }else{
            alert(`❌ failure to stop ModemManager.service ${data.message} `)

        }
    }else{
        if(startManagerModemService){
            alert("✅ Modem started correctly")
            document.getElementById('button3').style.display = 'none'; 
            document.getElementById('button1').style.display = 'block'; 
        }else{
            document.getElementById('button1').style.display = 'none'; 
            document.getElementById('button2').style.display = 'block';
            alert("✅ Modem stopped correctly")

        }
    }
}
async function deleteWhiteList() {
    if(confirm("¿Are you sure you want to delete the whiteList?")){
        const token = localStorage.getItem("access_token"); 

        var modemSelect = document.getElementById("modem");
  
        const response =await fetch(viewList, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`,  
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ modemSelect })

        });
        //La data traera el mensaje que usare en los alert
        const data = await response.json();
        if (!response.ok){
            alert(`❌ Failed to clear the whitelist: ${data.message}`)
        }else{
            alert(`✅ Whitelist successfully cleared: ${data.message}`)
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
            document.getElementById('button2').style.display = 'none'; // Oculta el segundo botón
            document.getElementById('button3').style.display = 'block'; // Muestra el tercer botón

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

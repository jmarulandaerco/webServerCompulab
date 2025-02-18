function loadContentModbus(option) {
    fetch(`/home/content/form/${option}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al cargar el contenido: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content3").innerHTML = data;
            console.log("Pase por aca?")
            loadFunction(option);

        })
        .catch(error => {
            console.log('Error al cargar el contenido:', error);
            document.getElementById("content3").innerHTML = "<h1>Error al cargar el contenido</h1>";
        });
}



function loadAddDevices() {
    fetch(viewAddDevices)  // Llamamos a la vista de Django
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            return response.json();  // Asumimos que la respuesta es un JSON
        })
        .then(data => {
            // Accedemos a la lista de dispositivos dentro de la propiedad "modbus_map"
            const modbusMapList = data.modbus_map;  // Aquí obtenemos la lista de opciones

            const modbusMapFolderSelect = document.getElementById("modbus_map_folder");
            
            // Limpiar las opciones previas (si existen)
            modbusMapFolderSelect.innerHTML = "";

            // Crear y agregar un "option" por cada dispositivo en la lista
            modbusMapList.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.value = option;  // El valor del "option" será el nombre del dispositivo
                optionElement.textContent = option;  // El texto visible será el nombre del dispositivo
                modbusMapFolderSelect.appendChild(optionElement);
            });
            console.log(modbusMapList)
        })
        .catch(error => {
            console.error("Error al cargar los dispositivos:", error);
        });
}

async function loadFormDataSettingModbus() {
    try {
        const response = await fetch(getFormDatasettingModbus);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
        const data = await response.json();
        document.getElementById("debug").value = data.debug;
        document.getElementById("attempts").value = data.attempts;
        document.getElementById("timeout").value = data.timeout;
    } catch (error) {
        console.error("Error:", error);
    }
}
async function loadFunctionModbus(option){
    switch (option) {
        case 'modbusSetting':
            loadFormDataSettingModbus();
            break;
       
        default:
            console.warn('Opción no reconocida:', option);
    }
    
}



function loadAddDevices() {
    fetch(viewAddDevices)  // Llamamos a la vista de Django
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            return response.json();  // Asumimos que la respuesta es un JSON
        })
        .then(data => {
            // Accedemos a la lista de dispositivos dentro de la propiedad "modbus_map"
            const modbusMapList = data.modbus_map;  // Aquí obtenemos la lista de opciones

            const modbusMapFolderSelect = document.getElementById("modbus_map_folder");
            
            // Limpiar las opciones previas (si existen)
            modbusMapFolderSelect.innerHTML = "";

            // Crear y agregar un "option" por cada dispositivo en la lista
            modbusMapList.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.value = option;  // El valor del "option" será el nombre del dispositivo
                optionElement.textContent = option;  // El texto visible será el nombre del dispositivo
                modbusMapFolderSelect.appendChild(optionElement);
            });
            console.log(modbusMapList)
        })
        .catch(error => {
            console.error("Error al cargar los dispositivos:", error);
        });
}


async function loadFormDataMeasureModbus() {
    try {
        const response = await fetch(getFormDataUrl);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
        const data = await response.json();
        console.log(data)
        document.getElementById("zone").value = data.zone;
        document.getElementById("modbus").value = data.modbus;
        document.getElementById("start").value = data.start;
        document.getElementById("stop").value = data.stop;
    } catch (error) {
        console.error("Error:", error);
    }
}

async function updateMeasureModbus() {
    const zone = document.getElementById("zone").value;
    const modbus = document.getElementById("modbus").value;
    const start = document.getElementById("start").value;
    const stop = document.getElementById("stop").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        console.log(getFormDataModemChecker)
        const response =  await fetch(getFormDataUrl, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ zone,modbus,start,stop })
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


async function loadFormDataModes() {
    try {
        const response = await fetch(getFormDataUrlServerModes);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
        const data = await response.json();

        document.getElementById("mode").value = data.mode;

        const limitationRadio = document.querySelector(`input[name="limitation"][value="${data.limitation}"]`);
        if (limitationRadio) {
            limitationRadio.checked = true;
        }

        const compensationRadio = document.querySelector(`input[name="compensation"][value="${data.compensation}"]`);
        if (compensationRadio) {
            compensationRadio.checked = true;
        }

        // Llenar los campos de sampling
        document.getElementById("sampling_limitation").value = data.sampling_limitation;
        document.getElementById("sampling_compensation").value = data.sampling_compensation;
    } catch (error) {
        console.error("Error:", error);
    }
}


async function updateDataModes() {
    const mode = document.getElementById("mode").value;
    const limitation = document.querySelector('input[name="limitation"]:checked')?.value;
    const compensation = document.querySelector('input[name="compensation"]:checked')?.value;
    const sampling_limitation = document.getElementById("sampling_limitation").value;
    const sampling_compensation =  document.getElementById("sampling_compensation").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        console.log(getFormDataModemChecker)
        const response =  await fetch(getFormDataUrlServerModes, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ mode,limitation,compensation,sampling_limitation,sampling_compensation })
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

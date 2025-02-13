    function loadContentMenu(option) {
    fetch(`/home/content/form/${option}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al cargar el contenido: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content2").innerHTML = data;
            loadFunction(option);
            
        })
        .catch(error => {
            console.log('Error al cargar el contenido:', error);
            document.getElementById("content2").innerHTML = "<h1>Error al cargar el contenido</h1>";
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

async function loadFormDataServerSelection() {
    try {
        const response = await fetch(getFormDataUrlServerSelection);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
        const data = await response.json();
        
        // Llenar los campos del formulario con los valores de ejemplo
        document.getElementById("server").value = data.Server;
        document.getElementById("neu_plus").value = data.neu_plus;
        document.getElementById("telemetry").value = data.telemetry;
        document.getElementById("mqtt").value = data.mqtt;
        document.getElementById("storage").value = data.storage;
    } catch (error) {
        console.error("Error:", error);
    }
}

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



async function loadFormDataSettingDatabase() {
    try {
        const response = await fetch(getFormDataUrlSettingDatabase);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
            const data = await response.json();
            document.getElementById("day").value = data.day;
            document.getElementById("await").value = data.await;
    } catch (error) {
        console.error("Error:", error);
    }
}

async function loadFormDataSettingInterface() {
    try {
        const response = await fetch(getFormDataUrlSettingInterface);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
            const data = await response.json();
            document.getElementById("interface").value = data.interface;
            document.getElementById("connection").value = data.connection;
    } catch (error) {
        console.error("Error:", error);
    }
}

async function loadFormDataAdvanced(){

}

async function loadFunction(option){
    switch (option) {
        case 'modbusMeasure':
            loadFormDataMeasureModbus();
            break;
        case 'serverSelection':
            loadFormDataServerSelection();
            break;
        case 'operationMode':
            loadFormDataModes();
            break;
        case 'databaseSetting':
            loadFormDataSettingDatabase();
            break;
        case 'networkSettings':
            loadFormDataSettingInterface();
            break;
        case 'advanced':
            loadFormDataAdvanced();
            break;
        default:
            console.warn('Opción no reconocida:', option);
    }
    
}
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


function loadContentSetting(option) {
    fetch(`/home/content/form/${option}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al cargar el contenido: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content5").innerHTML = data;
            loadFunctin(option);
            
        })
        .catch(error => {
            console.log('Error al cargar el contenido:', error);
            document.getElementById("content2").innerHTML = "<h1>Error al cargar el contenido</h1>";
        });
}
function loadContentHttp(option) {
    fetch(`/home/content/form/${option}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al cargar el contenido: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content4").innerHTML = data;
            loadFunction(option);
            
        })
        .catch(error => {
            console.log('Error al cargar el contenido:', error);
            document.getElementById("content4").innerHTML = "<h1>Error al cargar el contenido</h1>";
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


async function loadFormDataSettingLog() {
    try {
        const response = await fetch(getFormDatasettingLog);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
        const data = await response.json();
        console.log(data)
        document.getElementById("level").value = data.level;
        document.getElementById("stdout").value = data.stdout;
        document.getElementById("file").value = data.file;
        document.getElementById("enable").value = data.enable;
        document.getElementById("log_size").value = data.log_size;
        document.getElementById("backup").value = data.backup;

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
        console.log(data)
        // Llenar los campos del formulario con los valores de ejemplo
        document.getElementById("server").value = data.server;
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


async function loadFormDataSignalChecker() {
    try {
        const response = await fetch(getFormDataSignalChecker);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
            const data = await response.json();
            document.getElementById("onomondo").value = data.onomondo;
            document.getElementById("minimum").value = data.minimum;
    } catch (error) {
        console.error("Error:", error);
    }
}



async function loadFormDataModemChecker() {
    try {
        const response = await fetch(getFormDataModemChecker);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
            const data = await response.json();
            document.getElementById("connection").value = data.connection;
            document.getElementById("attemts").value = data.attemts;
    } catch (error) {
        console.error("Error:", error);
    }
}


async function loadFormDataServerChecker() {
    try {
        const response = await fetch(getFormDataServerChecker);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
            const data = await response.json();
            document.getElementById("requests").value = data.requests;
    } catch (error) {
        console.error("Error:", error);
    }
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
        case 'settingLog':
            loadFormDataSettingLog();
            break;
        case 'modemChecker':
            loadFormDataModemChecker();
            break;
        case 'serverChecker':
            loadFormDataServerChecker();
            break;
        case 'signalChecker':
            loadFormDataSignalChecker();
            break;
        default:
            break;

    }
    
}
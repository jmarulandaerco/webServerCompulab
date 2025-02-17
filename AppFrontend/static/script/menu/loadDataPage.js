let intervalId;

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

        })
        .catch(error => {
            console.log('Error al cargar el contenido:', error);
            document.getElementById("content5").innerHTML = "<h1>Error al cargar el contenido</h1>";
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
async function updateInformationDataSettingLog() {
    const level = document.getElementById("level").value;
    const stdout = document.getElementById("stdout").value;
    const file = document.getElementById("file").value;
    const enable = document.getElementById("enable").value;
    const log_size = document.getElementById("log_size").value;
    const backup = document.getElementById("backup").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        console.log(getFormDataModemChecker)
        const response = await fetch(getFormDatasettingLog, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ level, stdout, file, enable, log_size, backup })
        });

        const data = await response.json();

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

async function updateSettingInterface() {
    const interface = document.getElementById("interface").value;
    const connection = document.getElementById("connection").value;


    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        console.log(getFormDataModemChecker)
        const response = await fetch(getFormDataUrlSettingInterface, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ interface, connection})
        });

        const data = await response.json();

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
function loadContent(option) {
    // checkServiceStatus();
    fetch(`/home/content/${option}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error al cargar el contenido: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content").innerHTML = data;

            switch (option) {
                case "form/limitation":
                    loadFormDataLimitation();
                    break;

                case "form/compensation":
                    loadFormDataCompensation();
                    break;

                case "form/database":
                    loadFormDataBase();
                    break;
            }

            if (option === "logs") {

                document.getElementById("refreshButton").addEventListener("click", fetchLogs);

                intervalId = setInterval(fetchLogs, 5000);

            } else {
                if (intervalId) {
                    clearInterval(intervalId); // Detiene el intervalo si existe
                    intervalId = null; // Limpia la variable
                    console.log("Actualización automática detenida");
                }
            }

            // Remueve la clase 'active' de todos los enlaces del sidebar
            document.querySelectorAll("#sidebar a").forEach(a => a.classList.remove("active"));


            // Encuentra el enlace correspondiente y agrégale la clase 'active'
            document.querySelectorAll("#sidebar a").forEach(a => {
                if (a.getAttribute("onclick")?.includes(option)) {
                    a.classList.add("active");
                }
            });
        })
        .catch(error => {
            console.log('Error al cargar el contenido:', error);
            document.getElementById("content").innerHTML = "<h1>Error al cargar el contenido</h1>";
        });
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

async function updateServerSelection() {
    const server = document.getElementById("server").value;
    const neu_plus = document.getElementById("neu_plus").value;
    const telemetry = document.getElementById("telemetry").value;
    const mqtt = document.getElementById("mqtt").value;
    const storage = document.getElementById("storage").value;

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        console.log(getFormDataModemChecker)
        const response = await fetch(getFormDataUrlServerSelection, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ server, neu_plus, telemetry, mqtt, storage })
        });

        const data = await response.json();

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

async function loadFunction(option) {
    switch (option) {
        case 'modbusMeasure':
            loadFormDataMeasureModbus();
            break;
        case 'serverSelectionModbus':
            loadFormDataServerSelection();
            break;
        case 'operationModeModbus':
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
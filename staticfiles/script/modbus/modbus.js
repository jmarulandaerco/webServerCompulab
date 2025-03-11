function loadContentModbus(option) {
    fetch(`/home/content/form/modbus/${option}/`)
        .then(response => {
            if (!response.ok) {
                alert(`Error loading content: ${response.statusText}`);
            }
            return response.text();
        })
        .then(data => {
            document.getElementById("content3").innerHTML = data;
            loadFunction(option);

        })
        .catch(error => {
            document.getElementById("content3").innerHTML = "<h1>Error loading content</h1>";
        });
}

function loadDevices(page) {
    const fullUrl = `/api/modbus/devices/?device=${encodeURIComponent(page)}`; 
    fetch(fullUrl)  
        .then(response => {
            console.log(response);
            if (!response.ok) {
                alert(`Error: ${response.statusText}`);
            }
            return response.text();
        })
        .then(html => {
            document.getElementById("content3").innerHTML = html;
        })
        .catch(error => {
            console.error("Error while loading devices:", error);
            document.getElementById("content3").innerHTML = "<p>Error while loading devices</p>";
        });
}


async function loadFormDataSettingModbus() {
    try {
        const response = await fetch(getFormDatasettingModbus);
        if (!response.ok) {
            alert("Error loading data");
        }
        const data = await response.json();
        document.getElementById("debug").value = data.debug;
        document.getElementById("attempts").value = data.attempts;
        document.getElementById("timeout").value = data.timeout;
    } catch (error) {
        alert("Error:", error);
    }
}

//function for loading modbus map options
function handleSelectChange(event) {
    const modbusMapFolderSelect = document.getElementById("modbus_map_folder");
    const selectedValue = modbusMapFolderSelect.value;  
    fetch(mapFolder, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"

        },
        body: JSON.stringify({ selectedValue })

    })
        .then(response => response.json())
        .then(data => {
          
            const modbusMapList = data.data;

            const modbusMapFolderSelect = document.getElementById("modbus_map_json");

            modbusMapFolderSelect.innerHTML = "";

            modbusMapList.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.value = option;
                optionElement.textContent = option;
                modbusMapFolderSelect.appendChild(optionElement);
            });

            if (modbusMapList.length > 0) {
                modbusMapFolderSelect.value = modbusMapList[0];

                modbusMapFolderSelect.dispatchEvent(new Event("change"));
            }


        }).catch(error => {
            document.getElementById("content3").innerHTML = "<h1>Error loading content</h1>";
        });
}

function loadAddDevicesUpdateDevice(selectedDevice) {
    fetch(mapFolder)
        .then(response => {
            if (!response.ok) {
                alert(`Error: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const modbusMapList = data.modbus_map;
            const modbusMapFolderSelect = document.getElementById("modbus_map_folder");

            modbusMapFolderSelect.innerHTML = "";

            modbusMapList.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.value = option;
                optionElement.textContent = option;
                modbusMapFolderSelect.appendChild(optionElement);
            });

            if (selectedDevice && modbusMapList.includes(selectedDevice)) {
                modbusMapFolderSelect.value = selectedDevice;
            } else if (modbusMapList.length > 0) {
                modbusMapFolderSelect.value = modbusMapList[0];
            } else {
                alert("❌ No devices are available for selection.");
            }

            modbusMapFolderSelect.dispatchEvent(new Event("change"));
        })
        .catch(error => {
            console.error("Error while loading devices:", error);
        });
}

function loadAddDevices() {
    fetch(mapFolder)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            const modbusMapList = data.modbus_map;  // Aquí obtenemos la lista de opciones

            const modbusMapFolderSelect = document.getElementById("modbus_map_folder");

            modbusMapFolderSelect.innerHTML = "";

            modbusMapList.forEach(option => {
                const optionElement = document.createElement("option");
                optionElement.value = option;  // El valor del "option" será el nombre del dispositivo
                optionElement.textContent = option;  // El texto visible será el nombre del dispositivo
                modbusMapFolderSelect.appendChild(optionElement);
            });
            if (modbusMapList.length > 0) {
                modbusMapFolderSelect.value = modbusMapList[0];

                modbusMapFolderSelect.dispatchEvent(new Event("change"));
            }
        })
        .catch(error => {
            alert("Error while loading devices:", error);
        });
}

async function loadFormDataMeasureModbus() {
    try {
        const response = await fetch(getFormDataUrl);
        if (!response.ok) {
            alert("Error while loading devices");
        }
        const data = await response.json();
        document.getElementById("zone").value = data.zone;
        document.getElementById("modbus").value = data.modbus;
        document.getElementById("start").value = data.start;
        document.getElementById("stop").value = data.stop;
    } catch (error) {
        console.error("Error:", error);
    }
}

async function updateSettingModbus() {
    const log_debug = document.getElementById("debug").value;
    const max_attempts = document.getElementById("attempts").value;
    const timeout_attempts = document.getElementById("timeout").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        const response = await fetch(getFormDatasettingModbus, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken // Enviar CSRF token
            },
            body: JSON.stringify({ log_debug, max_attempts, timeout_attempts })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation"); // Muestra éxito si las contraseñas coinciden

        } else {
            alert("✅ " + data.message); // Muestra éxito si las contraseñas coinciden


        }

    } catch (error) {
        alert("❌ " + error.message); // Muestra error si las contraseñas no coinciden
        console.error("Error:", error);
    }
};

async function updateMeasureModbus() {
    const zone = document.getElementById("zone").value;
    const modbus = document.getElementById("modbus").value;
    const start = document.getElementById("start").value;
    const stop = document.getElementById("stop").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(getFormDataUrl, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ zone, modbus, start, stop })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation");

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
    }
};

async function loadFormDataModes() {
    try {
        const response = await fetch(getFormDataUrlServerModes);
        if (!response.ok) {
            alert("Error while loading data");
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
    const sampling_compensation = document.getElementById("sampling_compensation").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value; // Obtiene el CSRF token

    try {
        const response = await fetch(getFormDataUrlServerModes, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ mode, limitation, compensation, sampling_limitation, sampling_compensation })
        });

        const data = await response.json();

        if (!response.ok) {

            alert("❌ " + "Error in validation");

        } else {
            alert("✅ " + data.message);


        }

    } catch (error) {
        alert("❌ " + error.message);
        console.error("Error:", error);
    }
};

async function addDeviceRtu() {
    try {
        const nameDevice = document.getElementById("name").value;
        const portDevice = document.getElementById("port").value;
        const baudrate = document.getElementById("baudrate").value;
        const initial = document.getElementById("initial").value;
        const end = document.getElementById("end").value;
        const modbus_function = document.getElementById("modbus_function").value;
        const initial_address = document.getElementById("initial_address").value;
        const total_registers = document.getElementById("total_registers").value;
        const modbus_map_folder = document.getElementById("modbus_map_folder").value;
        const modbus_map_json = document.getElementById("modbus_map_json").value;
        const modbus_mode = document.getElementById("modbus_mode").value;
        const device_type = document.getElementById("device_type").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const save_db = document.getElementById("save_db").value;
        const server_send = document.getElementById("server_send").value;

        const response = await fetch(viewAddRtu, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                nameDevice, portDevice, baudrate, initial, end, modbus_function,
                initial_address, total_registers, modbus_map_folder, modbus_map_json,
                modbus_mode, device_type, save_db, server_send
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            await loadDevices('seeDevices');
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}

async function addDeviceTcp() {
    try {
        const nameDevice = document.getElementById("name").value;
        const ip_device = document.getElementById("ip_device").value;
        const port_device = document.getElementById("port_device").value;
        const offset = document.getElementById("offset").value;
        const initial = document.getElementById("initial").value;
        const end = document.getElementById("end").value;
        const modbus_function = document.getElementById("modbus_function").value;
        const initial_address = document.getElementById("initial_address").value;
        const total_registers = document.getElementById("total_registers").value;
        const modbus_map_folder = document.getElementById("modbus_map_folder").value;
        const modbus_map_json = document.getElementById("modbus_map_json").value;
        const modbus_mode = document.getElementById("modbus_mode").value;
        const device_type = document.getElementById("device_type").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const save_db = document.getElementById("save_db").value;
        const server_send = document.getElementById("server_send").value;

        const response = await fetch(viewAddTcp, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                nameDevice, ip_device, port_device, offset, initial, end, modbus_function,
                initial_address, total_registers, modbus_map_folder, modbus_map_json,
                modbus_mode, device_type, save_db, server_send
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            await loadDevices('seeDevices');
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}

async function deleteDevice(device) {
    try {
        console.log(device)
        if (confirm("Are you sure to erase the device?")) {
            const response = await fetch(mapFolder, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ device })
            });

            const result = await response.json();

            if (!response.ok) {
                alert("❌ Error in validation: " + result.message);
            } else {
                alert("✅ " + result.message);
                await loadDevices('seeDevices');
            }
        }
    } catch (error) {
        console.error("Error in deletion:", error.message);
    }
}

async function ModifyOption(device) {
    try {
        let url = device.includes("RTU")
            ? "/home/content/form/modbus/updateDeviceRtu/"
            : "/home/content/form/modbus/updateDeviceTcp/";

        const response = await fetch(url);

        if (!response.ok) {
            alert("❌ Error in validation: " + response.message);
        }

        const data = await response.text();
        document.getElementById("content3").innerHTML = data;
        loadAddDevices();

        if (device.includes("RTU")) {
            const responseDevice = await fetch(`${modifyDevice}?device=${encodeURIComponent(device)}`);


            if (!responseDevice.ok) {
                alert(" ❌ Error while loading the data device Rtu");
            }
            const dataRtu = await responseDevice.json();
            document.getElementById("nameRtu").value = dataRtu.nameRtu;
            document.getElementById("portRtu").value = dataRtu.portRtu;
            document.getElementById("baudrateRtu").value = dataRtu.baudrateRtu;
            document.getElementById("initialRtu").value = dataRtu.initialRtu;
            document.getElementById("endRtu").value = dataRtu.endRtu;
            document.getElementById("modbus_function_rtu").value = dataRtu.modbus_function_rtu;
            document.getElementById("initial_address_rtu").value = dataRtu.initial_address_rtu;
            document.getElementById("total_registers_rtu").value = dataRtu.total_registers_rtu;
            document.getElementById("modbus_map_folder").value = dataRtu.modbus_map_folder_rtu;
            loadAddDevicesUpdateDevice(dataRtu.modbus_map_folder_rtu)
            document.getElementById("modbus_map_json").value = dataRtu.modbus_map_json_rtu;
            document.getElementById("modbus_mode_rtu").value = dataRtu.modbus_mode_rtu;
            document.getElementById("device_type_rtu").value = dataRtu.device_type_rtu;
            document.getElementById("save_db_rtu").value = dataRtu.save_db_rtu;
            document.getElementById("server_send_rtu").value = dataRtu.server_send_rtu;
        } else {
            const responseDevice = await fetch(`${modifyDevice}?device=${encodeURIComponent(device)}`);


            if (!responseDevice.ok) {
                alert(" ❌  Error while loading the data device Rtu");
            }
            const dataRtu = await responseDevice.json();
            document.getElementById("nameTcp").value = dataRtu.nameTcp;
            document.getElementById("ip_device_tcp").value = dataRtu.ip_device_tcp;
            document.getElementById("port_device_tcp").value = dataRtu.port_device_tcp;
            document.getElementById("offset_tcp").value = dataRtu.offset_tcp;
            document.getElementById("initial_tcp").value = dataRtu.initial_tcp;
            document.getElementById("end_tcp").value = dataRtu.end_tcp;
            document.getElementById("modbus_function_tcp").value = dataRtu.modbus_function_tcp;
            document.getElementById("initial_address_tcp").value = dataRtu.initial_address_tcp;
            document.getElementById("total_registers_tcp").value = dataRtu.total_registers_tcp;
            document.getElementById("modbus_map_folder").value = dataRtu.modbus_map_folder_tcp;
            loadAddDevicesUpdateDevice(dataRtu.modbus_map_folder_tcp)
            document.getElementById("modbus_map_json").value = dataRtu.modbus_map_json_tcp;
            document.getElementById("modbus_mod_tcp").value = dataRtu.modbus_mod_tcp;
            document.getElementById("device_type_tcp").value = dataRtu.device_type_tcp;
            document.getElementById("save_db_tcp").value = dataRtu.save_db_tcp;
            document.getElementById("server_send_tcp").value = dataRtu.server_send_tcp;


        }


    } catch (error) {
        document.getElementById("content3").innerHTML = "<h1>Error al cargar el contenido</h1>";
    }
}

async function updateDeviceTcp() {
    try {
        const nameDevice = document.getElementById("nameTcp").value;
        const ip_device = document.getElementById("ip_device_tcp").value;
        const port_device = document.getElementById("port_device_tcp").value;
        const offset = document.getElementById("offset_tcp").value;
        const initial = document.getElementById("initial_tcp").value;
        const end = document.getElementById("end_tcp").value;
        const modbus_function = document.getElementById("modbus_function_tcp").value;
        const initial_address = document.getElementById("initial_address_tcp").value;
        const total_registers = document.getElementById("total_registers_tcp").value;
        const modbus_map_folder = document.getElementById("modbus_map_folder").value;
        const modbus_map_json = document.getElementById("modbus_map_json").value;
        const modbus_mode = document.getElementById("modbus_mod_tcp").value;
        const device_type = document.getElementById("device_type_tcp").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const save_db = document.getElementById("save_db_tcp").value;
        const server_send = document.getElementById("server_send_tcp").value;

        const response = await fetch(viewAddTcp, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                nameDevice, ip_device, port_device, offset, initial, end, modbus_function,
                initial_address, total_registers, modbus_map_folder, modbus_map_json,
                modbus_mode, device_type, save_db, server_send
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            await loadDevices('seeDevices');
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}

async function updateDeviceRtu() {
    try {
        const nameDevice = document.getElementById("nameRtu").value;
        const portDevice = document.getElementById("portRtu").value;
        const baudrate = document.getElementById("baudrateRtu").value;
        const initial = document.getElementById("initialRtu").value;
        const end = document.getElementById("endRtu").value;
        const modbus_function = document.getElementById("modbus_function_rtu").value;
        const initial_address = document.getElementById("initial_address_rtu").value;
        const total_registers = document.getElementById("total_registers_rtu").value;
        const modbus_map_folder = document.getElementById("modbus_map_folder").value;
        const modbus_map_json = document.getElementById("modbus_map_json").value;
        const modbus_mode = document.getElementById("modbus_mode_rtu").value;
        const device_type = document.getElementById("device_type_rtu").value;
        const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

        const save_db = document.getElementById("save_db_rtu").value;
        const server_send = document.getElementById("server_send_rtu").value;

        const response = await fetch(viewAddRtu, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                nameDevice, portDevice, baudrate, initial, end, modbus_function,
                initial_address, total_registers, modbus_map_folder, modbus_map_json,
                modbus_mode, device_type, save_db, server_send
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert("❌ Error in validation: " + data.message);
        } else {
            alert("✅ " + data.message);
            await loadDevices('seeDevices');
        }

    } catch (error) {
        alert("❌ Error: " + error.message);
        console.error("Error:", error);
    }
}




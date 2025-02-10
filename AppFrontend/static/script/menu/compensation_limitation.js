async function loadFormDataLimitation() {
    try {
        const response = await fetch(getFormDataLimitation);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
            const data = await response.json();
           

            const limitationRadio = document.querySelector(`input[name="energy_meter"][value="${data.limitation}"]`);
            if (limitationRadio) {
                limitationRadio.checked = true;
            }

            
            document.getElementById("meter_ids").value = data.meter_ids;
            document.getElementById("inverter_ids").value = data.inverter_ids;
            document.getElementById("porcentage").value = data.porcentage;
            document.getElementById("grid_min").value = data.inverter_ids;
            document.getElementById("grid_max").value = data.meter_ids;
            document.getElementById("inverter_min").value = data.inverter_ids;
            document.getElementById("inverterMax").value = data.inverterMax;
            
    } catch (error) {
        console.error("Error:", error);
    }
}


async function loadFormDataCompensation() {
    try {
        const response = await fetch(getFormDataCompensation);
        if (!response.ok) {
            throw new Error("Error al cargar los datos");
        }
            const data = await response.json();
           

            const compensation = document.querySelector(`input[name="reactive_power"][value="${data.reactive_power}"]`);
            if (compensation) {
                compensation.checked = true;
            }

            
            document.getElementById("meter_ids").value = data.meter_ids;
            document.getElementById("smart_logger").value = data.smart_logger;
            document.getElementById("high").value = data.high;
            document.getElementById("low").value = data.low;
            document.getElementById("reactive").value = data.reactive;
            document.getElementById("active").value = data.active;
            document.getElementById("time").value = data.time;
            document.getElementById("factor").value = data.factor;
            
    } catch (error) {
        console.error("Error:", error);
    }
}


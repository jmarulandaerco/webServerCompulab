async function loadFormDataLimitation() {
    try {
        const response = await fetch(getFormDataLimitation);
        if (!response.ok) {
            alert("Error in loading the data");
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
            alert("Error in loading the data");
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
async function updateInformationLimitation() {
    const selectedValue = document.querySelector('input[name="energy_meter"]:checked')?.value;
    const meter_ids = document.getElementById("meter_ids").value;
    const inverter_ids = document.getElementById("inverter_ids").value;
    const porcentage = document.getElementById("porcentage").value;
    const grid_min = document.getElementById("grid_min").value;
    const grid_max = document.getElementById("grid_max").value;
    const inverter_min = document.getElementById("inverter_min").value;
    const inverterMax = document.getElementById("inverterMax").value;


    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(getFormDataLimitation, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ selectedValue, meter_ids, inverter_ids, porcentage, grid_min, grid_max, inverter_min, inverterMax })
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
async function updateInformationCompensation() {
    const selectedValue = document.querySelector('input[name="reactive_power"]:checked')?.value;
    const meter_ids = document.getElementById("meter_ids").value;
    const smart_logger = document.getElementById("smart_logger").value;
    const high = document.getElementById("high").value;
    const low = document.getElementById("low").value;
    const reactive = document.getElementById("reactive").value;
    const active = document.getElementById("active").value;
    const time = document.getElementById("time").value;
    const factor = document.getElementById("factor").value;
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    try {
        const response = await fetch(getFormDataCompensation, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ selectedValue, meter_ids, smart_logger, high, low, reactive, active, time, factor })
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
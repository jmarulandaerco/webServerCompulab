/**
 * Loads form data for the energy meter limitation configuration.
 * 
 * This function sends a GET request to the server to retrieve the energy meter limitation data. 
 * It populates the form fields with the retrieved values, including the meter IDs, inverter IDs, percentage, 
 * grid and inverter limits. It also sets the appropriate radio button based on the retrieved limitation value.
 * If the request is successful, the form fields are updated with the corresponding data. 
 * If an error occurs during the request or while processing the data, an error message is logged to the console.
 * 
 * @async
 * @function
 * 
 * @returns {void} This function does not return a value. It updates the DOM with the fetched limitation settings.
 * 
 * @throws {Error} Throws an error if there is an issue with the network request or processing the response.
 * 
 * @example
 * loadFormDataLimitation(); // Fetches and populates the form with energy meter limitation data.
 */

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

/**
 * Loads form data for the energy meter limitation configuration.
 * 
 * This function sends a GET request to the server to retrieve the energy meter limitation data. 
 * It populates the form fields with the retrieved values, including the meter IDs, inverter IDs, percentage, 
 * grid and inverter limits. It also sets the appropriate radio button based on the retrieved limitation value.
 * If the request is successful, the form fields are updated with the corresponding data. 
 * If an error occurs during the request or while processing the data, an error message is logged to the console.
 * 
 * @async
 * @function
 * 
 * @returns {void} This function does not return a value. It updates the DOM with the fetched limitation settings.
 * 
 * @throws {Error} Throws an error if there is an issue with the network request or processing the response.
 * 
 * @example
 * loadFormDataLimitation(); // Fetches and populates the form with energy meter limitation data.
 */

async function loadFormDataCompensation() {
    try {
        const response = await fetch(getFormDataCompensation);
        if (!response.ok) {
            alert("❌" + " "+response.message);
        }
        const data = await response.json();

        // const compensation = document.querySelector(`input[name="reactive_power"][value="${data.reactive_power}"]`);
        // if (compensation) {
        //     compensation.checked = true;
        // }
        console.log(data);
        document.getElementById("kindCompensation").value =data.kind;
        document.getElementById("meter_ids").value = data.meter_ids;
        document.getElementById("device_id").value=data.device
        document.getElementById("high").value = data.high;
        document.getElementById("low").value = data.low;
        document.getElementById("hightBand").value = data.band_high;
        document.getElementById("lowBand").value = data.band_low;
        document.getElementById("reactive").value = data.reactive;
        document.getElementById("active").value = data.active;
        document.getElementById("time").value = data.time;
        document.getElementById("factor").value = data.factor;

    } catch (error) {
        console.error("Error:", error);
    }
}


/**
 * Updates the energy meter limitation configuration based on user input.
 * 
 * This function sends a PUT request to the server to update the energy meter limitation settings. 
 * It collects values from the form inputs, including the selected limitation type, meter IDs, inverter IDs, 
 * percentage, and grid/inverter limits. The function sends these values in a JSON format to the server 
 * for processing. If the request is successful, a confirmation message is displayed. If there's an error 
 * during the request or validation, an error message is shown.
 * 
 * @async
 * @function
 * 
 * @returns {void} This function does not return a value. It triggers an alert based on the success or failure of the operation.
 * 
 * @throws {Error} Throws an error if there is an issue with the network request or processing the response.
 * 
 * @example
 * updateInformationLimitation(); // Updates the energy meter limitation settings based on form data.
 */

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

/**
 * Updates the compensation configuration for the reactive and active power settings.
 * 
 * This function sends a PUT request to the server to update the compensation settings based on the user input.
 * It gathers values from form fields, including the selected reactive power type, meter IDs, smart logger setting, 
 * high/low compensation thresholds, reactive power, active power, time, and compensation factor. These values are then 
 * sent as a JSON object in the body of the PUT request. If the update is successful, a success message is shown. 
 * If there is any error during the update or validation process, an error message is displayed.
 * 
 * @async
 * @function
 * 
 * @returns {void} This function does not return a value. It triggers an alert based on the success or failure of the operation.
 * 
 * @throws {Error} Throws an error if there is an issue with the network request or processing the response.
 * 
 * @example
 * updateInformationCompensation(); // Updates the compensation configuration with the form data.
 */

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
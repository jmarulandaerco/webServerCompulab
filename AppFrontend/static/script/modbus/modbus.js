function loadContentModbus(page) {
    fetch(`/home/content/form/${page}/`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('content3').innerHTML = html;
            loadFunctionModbus(page)
        })
        .catch(error => {
            document.getElementById("content3").innerHTML = "<h1>Error al cargar el contenido</h1>";
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
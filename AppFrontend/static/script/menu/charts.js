// function showGraphic() {
//     console.log("Click en botón");

//     const canvas = document.getElementById('miGrafica');
//     canvas.style.display = 'block';

//     const ctx = canvas.getContext('2d');

//     // Si ya existe una gráfica y es instancia de Chart, la destruimos
//     if (window.miGrafica instanceof Chart) {
//         window.miGrafica.destroy();
//     }

//     // Crear nueva gráfica
//     window.miGrafica = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: ['Router', 'Switch', 'Servidor'],
//             datasets: [{
//                 label: 'Dispositivos',
//                 data: [10, 7, 3],
//                 backgroundColor: [
//                     'rgba(255, 99, 132, 0.6)',
//                     'rgba(54, 162, 235, 0.6)',
//                     'rgba(75, 192, 192, 0.6)'
//                 ],
//                 borderColor: [
//                     'rgba(255, 99, 132, 1)',
//                     'rgba(54, 162, 235, 1)',
//                     'rgba(75, 192, 192, 1)'
//                 ],
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             responsive: true,
//             scales: {
//                 y: {
//                     beginAtZero: true
//                 }
//             }
//         }
//     });
// }


async function showGraphic() {
    const response = await fetch(ram);
    const data = await response.json();

    const canvas = document.getElementById('myChart');
    canvas.style.display = 'block';

    const ctx = canvas.getContext('2d');

    // Preparar datos para gráfica
    const labels = ['Total', 'Usada', 'Libre', 'Compartida', 'Buffer/Cache', 'Disponible'];
    const values = [
        parseMem(data.memoria.total),
        parseMem(data.memoria.usada),
        parseMem(data.memoria.libre),
        parseMem(data.memoria.compartida),
        parseMem(data.memoria.buffer_cache),
        parseMem(data.memoria.disponible)
    ];

    if (window.myChart instanceof Chart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Memoria (MB)',
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(73, 189, 0, 0.6)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Función para convertir strings como "945Mi" o "1.5Gi" a MB
function parseMem(value) {
    if (!value) return 0;
    const united = value.slice(-2).toUpperCase(); // Mi, Gi, Ki ...
    const number = parseFloat(value.slice(0, -2).replace(',', '.'));

    switch (united) {
        case 'KI': return number / 1024;
        case 'MI': return number;
        case 'GI': return number * 1024;
        case 'TI': return number * 1024 * 1024;
        default: return number; // en bytes o desconocido
    }
}

async function showTopCPUProcesses() {
    const response = await fetch(use);  // Cambie por su URL real
    const data = await response.json();

    const canvas = document.getElementById('myChart');
    canvas.style.display = 'block';

    const ctx = canvas.getContext('2d');

    // Preparar etiquetas y valores de CPU y MEM
    const labels = data.top_processes.map(p => `${p.command} (PID ${p.pid})`);
    const cpuValues = data.top_processes.map(p => p.cpu);
    const memValues = data.top_processes.map(p => p.mem);

    if (window.myChart instanceof Chart) {
        window.myChart.destroy();
    }

    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'CPU (%)',
                    data: cpuValues,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(73, 189, 0, 0.6)',
                    borderWidth: 1
                },
                {
                    label: 'Memoria (%)',
                    data: memValues,
                    backgroundColor: 'rgba(192, 75, 75, 0.6)',
                    borderColor: 'rgba(189, 73, 73, 0.6)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

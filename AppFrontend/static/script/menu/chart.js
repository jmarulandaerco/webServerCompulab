function showGraphic() {
    const canvas = document.getElementById('miGrafica');
    canvas.style.display = 'block'; // Muestra el canvas si estaba oculto

    // Evitar múltiples gráficas
    if (window.miGrafica) return;

    const ctx = canvas.getContext('2d');

    window.miGrafica = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Router', 'Switch', 'Servidor', 'Cámara', 'Sensor'],
            datasets: [{
                label: 'Cantidad de Dispositivos',
                data: [10, 7, 3, 8, 5],
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
function showGraphic() {
            console.log("Click en botón");

            const canvas = document.getElementById('miGrafica');
            canvas.style.display = 'block';

            const ctx = canvas.getContext('2d');

            // Evitar múltiples instancias
            if (window.miGrafica) {
                window.miGrafica.destroy();
            }

            window.miGrafica = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Router', 'Switch', 'Servidor'],
                    datasets: [{
                        label: 'Dispositivos',
                        data: [10, 7, 3],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.6)',
                            'rgba(54, 162, 235, 0.6)',
                            'rgba(75, 192, 192, 0.6)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(75, 192, 192, 1)'
                        ],
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
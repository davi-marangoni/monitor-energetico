// Dashboard functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize machines chart (top 5 by consumption)
    const machineCtx = document.getElementById('machinesChart');
    if (machineCtx) {
        new Chart(machineCtx, {
            type: 'bar',
            data: {
                labels: ['Máquina 1', 'Máquina 2', 'Máquina 3', 'Máquina 4', 'Máquina 5'],
                datasets: [{
                    label: 'Consumo (Watts)',
                    data: [85, 72, 65, 58, 42],
                    backgroundColor: [
                        '#3498db',
                        '#2ecc71',
                        '#f39c12',
                        '#e74c3c',
                        '#9b59b6'
                    ],
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Consumo (W)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                }
            }
        });
    }
    
    // Initialize consumption chart (line chart over time)
    const consumptionCtx = document.getElementById('consumptionChart');
    if (consumptionCtx) {
        new Chart(consumptionCtx, {
            type: 'line',
            data: {
                labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '23:59'],
                datasets: [{
                    label: 'Consumo Total (W)',
                    data: [320, 280, 450, 520, 480, 410, 350],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true,
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Consumo (W)'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'bottom'
                    }
                }
            }
        });
    }
});

// Machine detail page functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize CPU chart
    const cpuCtx = document.getElementById('cpuChart');
    if (cpuCtx) {
        new Chart(cpuCtx, {
            type: 'line',
            data: {
                labels: generateTimeLabels(24),
                datasets: [{
                    label: 'CPU (%)',
                    data: generateRandomData(24, 100),
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
                        max: 100
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
    
    // Initialize RAM chart
    const ramCtx = document.getElementById('ramChart');
    if (ramCtx) {
        new Chart(ramCtx, {
            type: 'line',
            data: {
                labels: generateTimeLabels(24),
                datasets: [{
                    label: 'RAM (GB)',
                    data: generateRandomData(24, 16),
                    borderColor: '#2ecc71',
                    backgroundColor: 'rgba(46, 204, 113, 0.1)',
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
                        max: 16
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
    
    // Initialize consumption chart
    const consumptionCtx = document.getElementById('consumptionChart');
    if (consumptionCtx) {
        new Chart(consumptionCtx, {
            type: 'line',
            data: {
                labels: generateTimeLabels(24),
                datasets: [{
                    label: 'Consumo (W)',
                    data: generateRandomData(24, 200),
                    borderColor: '#e74c3c',
                    backgroundColor: 'rgba(231, 76, 60, 0.1)',
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
                        beginAtZero: true
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
    
    // Setup filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const filter = this.getAttribute('data-filter');
            console.log('Filter applied:', filter);
            // Here you would fetch data based on the filter
        });
    });
});

// Helper functions
function generateTimeLabels(count) {
    const labels = [];
    for (let i = 0; i < count; i++) {
        const date = new Date();
        date.setHours(date.getHours() - (count - i));
        labels.push(date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }));
    }
    return labels;
}

function generateRandomData(count, max) {
    const data = [];
    for (let i = 0; i < count; i++) {
        data.push(Math.floor(Math.random() * max * 0.8 + max * 0.1));
    }
    return data;
}

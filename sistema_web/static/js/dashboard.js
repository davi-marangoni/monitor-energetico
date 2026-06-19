// Dashboard functionality

document.addEventListener('DOMContentLoaded', async function() {
    if (!window.utils || !window.authTokens || !window.authTokens.access) {
        return;
    }

    try {
        const [rankingResponse, consumoResponse] = await Promise.all([
            window.utils.apiFetch('/api/dashboard/ranking/'),
            window.utils.apiFetch('/api/dashboard/consumo-geral/?filtro=ultimas_24_horas'),
        ]);

        if (rankingResponse.ok) {
            const rankingData = await rankingResponse.json();
            renderMachinesChart(rankingData.top || []);
        }

        if (consumoResponse.ok) {
            const consumoData = await consumoResponse.json();
            renderConsumptionChart(consumoData.labels || [], consumoData.values || []);
        }
    } catch (error) {
        console.error('Erro ao carregar dashboard:', error);
    }
});

function renderMachinesChart(topMachines) {
    const machineCtx = document.getElementById('machinesChart');
    if (!machineCtx) return;

    new Chart(machineCtx, {
        type: 'bar',
        data: {
            labels: topMachines.map(item => item.hostname),
            datasets: [{
                label: 'Consumo (Watts)',
                data: topMachines.map(item => item.consumption || 0),
                backgroundColor: ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6'],
                borderRadius: 4,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Consumo (W)' },
                },
            },
            plugins: {
                legend: { display: true, position: 'bottom' },
            },
        },
    });
}

function renderConsumptionChart(labels, values) {
    const consumptionCtx = document.getElementById('consumptionChart');
    if (!consumptionCtx) return;

    new Chart(consumptionCtx, {
        type: 'line',
        data: {
            labels: labels.length ? labels : ['Sem dados'],
            datasets: [{
                label: 'Consumo Total (W)',
                data: values.length ? values : [0],
                borderColor: '#3498db',
                backgroundColor: 'rgba(52, 152, 219, 0.1)',
                tension: 0.4,
                fill: true,
                borderWidth: 2,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: { display: true, text: 'Consumo (W)' },
                },
            },
            plugins: {
                legend: { display: true, position: 'bottom' },
            },
        },
    });
}

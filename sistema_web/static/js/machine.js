// Machine detail page functionality

let cpuChart = null;
let ramChart = null;
let consumptionChart = null;

document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.machine-detail');
    if (!container) return;

    const maquinaId = container.dataset.maquinaId;
    loadMachineData(maquinaId, 'ultimas_24_horas');

    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            loadMachineData(maquinaId, this.getAttribute('data-filter'));
        });
    });

    const defaultFilter = document.querySelector('.filter-btn[data-filter="ultimas_24_horas"]');
    if (defaultFilter) {
        defaultFilter.classList.add('active');
    }
});

async function loadMachineData(maquinaId, filtro) {
    try {
        const response = await window.utils.apiFetch(
            `/api/telemetrias/historico/?maquina_id=${maquinaId}&filtro=${filtro}`
        );
        if (!response.ok) {
            throw new Error('Falha ao carregar histórico');
        }

        const data = await response.json();
        updateCharts(data);
    } catch (error) {
        console.error('Erro ao carregar dados da máquina:', error);
    }
}

function updateCharts(data) {
    const labels = data.map(item => {
        const date = new Date(item.coletado_em);
        return date.toLocaleString('pt-BR', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' });
    });
    const cpuData = data.map(item => item.percentual_uso_cpu);
    const ramData = data.map(item => item.ram_utilizada_gb);
    const consumptionData = data.map(item => item.consumo_total || 0);

    cpuChart = renderOrUpdateChart(cpuChart, 'cpuChart', 'CPU (%)', labels, cpuData, '#3498db', 'rgba(52, 152, 219, 0.1)', 100);
    ramChart = renderOrUpdateChart(ramChart, 'ramChart', 'RAM (GB)', labels, ramData, '#2ecc71', 'rgba(46, 204, 113, 0.1)', null);
    consumptionChart = renderOrUpdateChart(consumptionChart, 'consumptionChart', 'Consumo (W)', labels, consumptionData, '#e74c3c', 'rgba(231, 76, 60, 0.1)', null);
}

function renderOrUpdateChart(existingChart, canvasId, label, labels, data, color, bgColor, maxY) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return existingChart;

    const config = {
        type: 'line',
        data: {
            labels: labels.length ? labels : ['Sem dados'],
            datasets: [{
                label,
                data: data.length ? data : [0],
                borderColor: color,
                backgroundColor: bgColor,
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
                    max: maxY || undefined,
                },
            },
            plugins: {
                legend: { display: true, position: 'bottom' },
            },
        },
    };

    if (existingChart) {
        existingChart.data = config.data;
        existingChart.update();
        return existingChart;
    }

    return new Chart(canvas, config);
}

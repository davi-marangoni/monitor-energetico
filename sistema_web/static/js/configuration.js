// Configuration page functionality

document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.configuration');
    const form = document.querySelector('.energy-form');
    if (!form || !container) return;

    const configId = container.dataset.configId;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const payload = {
            tdp_cpu_watts: parseFloat(document.querySelector('#tdp').value),
            fator_idle_alpha: parseFloat(document.querySelector('#idle_factor').value),
            consumo_ram_por_gb: parseFloat(document.querySelector('#ram_consumption').value),
            ativo: document.querySelector('#ativo').checked,
        };

        try {
            const response = await window.utils.apiFetch(
                `/api/configuracoes-energeticas/${configId}/`,
                {
                    method: 'PATCH',
                    body: JSON.stringify(payload),
                }
            );

            if (!response.ok) {
                throw new Error('Falha ao salvar configuração');
            }

            showMessage('Configuração salva com sucesso!', 'success');
            updateFormulaExample();
        } catch (error) {
            console.error(error);
            showMessage('Erro ao salvar configuração.', 'danger');
        }
    });

    const inputs = document.querySelectorAll('input[type="number"]');
    inputs.forEach(input => {
        input.addEventListener('change', updateFormulaExample);
        input.addEventListener('input', updateFormulaExample);
    });
});

function updateFormulaExample() {
    const tdp = parseFloat(document.querySelector('#tdp').value) || 0;
    const idleFactor = parseFloat(document.querySelector('#idle_factor').value) || 0;
    const ramConsumption = parseFloat(document.querySelector('#ram_consumption').value) || 0;

    const formulaSection = document.querySelector('.formula');
    if (formulaSection) {
        const tdpLine = formulaSection.querySelector('p:nth-child(2)');
        if (tdpLine) {
            tdpLine.textContent = `Consumo_CPU = ${tdp} × (${idleFactor} + (1 − ${idleFactor}) × Uso_CPU / 100)`;
        }

        const ramLine = formulaSection.querySelector('p:nth-child(4)');
        if (ramLine) {
            ramLine.textContent = `Consumo_RAM = RAM_Utilizada × ${ramConsumption}`;
        }
    }
}

function showMessage(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    const container = document.querySelector('main.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        setTimeout(() => {
            alertDiv.style.opacity = '0';
            alertDiv.style.transition = 'opacity 0.3s';
            setTimeout(() => {
                alertDiv.remove();
            }, 300);
        }, 5000);
    }
}

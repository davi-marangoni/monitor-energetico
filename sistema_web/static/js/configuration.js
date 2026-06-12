// Configuration page functionality

document.addEventListener('DOMContentLoaded', function() {
    // Setup form submission
    const form = document.querySelector('.energy-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const tdp = document.querySelector('#tdp').value;
            const idleFactor = document.querySelector('#idle_factor').value;
            const ramConsumption = document.querySelector('#ram_consumption').value;
            const ativo = document.querySelector('#ativo').checked;
            
            console.log('Form data:', {
                tdp_cpu_watts: tdp,
                fator_idle_alpha: idleFactor,
                consumo_ram_por_gb: ramConsumption,
                ativo: ativo
            });
            
            // Show success message
            showMessage('Configuração salva com sucesso!', 'success');
        });
    }
    
    // Update formula example when inputs change
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

// Utility functions and global scripts

// Add CSRF token to all AJAX requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Setup AJAX headers
function setupAjax() {
    const csrftoken = getCookie('csrftoken');
    
    fetch.defaults = {
        headers: {
            'X-CSRFToken': csrftoken
        }
    };
}

// Format date to Brazilian format
function formatDate(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

// Format date to ISO string
function formatDateISO(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toISOString();
}

// Close alerts after some time
function setupAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
    });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    setupAjax();
    setupAlerts();
});

// Export functions for use in other scripts
window.utils = {
    getCookie,
    formatDate,
    formatDateISO,
    setupAjax,
    setupAlerts
};

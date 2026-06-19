// Utility functions and global scripts

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

async function refreshAccessToken() {
    if (!window.authTokens || !window.authTokens.refresh) {
        throw new Error('Refresh token indisponível');
    }

    const response = await fetch('/api/autenticacao/refresh', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: window.authTokens.refresh }),
    });

    if (!response.ok) {
        throw new Error('Falha ao renovar token');
    }

    const data = await response.json();
    window.authTokens.access = data.access;
    if (data.refresh) {
        window.authTokens.refresh = data.refresh;
    }
    return data.access;
}

async function apiFetch(url, options = {}) {
    const headers = {
        'Content-Type': 'application/json',
        ...(options.headers || {}),
    };

    if (window.authTokens && window.authTokens.access) {
        headers['Authorization'] = `Bearer ${window.authTokens.access}`;
    }

    let response = await fetch(url, { ...options, headers });

    if (response.status === 401 && window.authTokens && window.authTokens.refresh) {
        try {
            await refreshAccessToken();
            headers['Authorization'] = `Bearer ${window.authTokens.access}`;
            response = await fetch(url, { ...options, headers });
        } catch (error) {
            window.location.href = '/login';
            throw error;
        }
    }

    return response;
}

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

function formatDateISO(date) {
    if (typeof date === 'string') {
        date = new Date(date);
    }
    return date.toISOString();
}

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

document.addEventListener('DOMContentLoaded', function() {
    setupAlerts();
});

window.utils = {
    getCookie,
    formatDate,
    formatDateISO,
    apiFetch,
    refreshAccessToken,
    setupAlerts,
};

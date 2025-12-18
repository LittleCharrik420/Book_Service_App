// ========== Authentication & Navigation ==========

function checkAuthStatus() {
    const token = localStorage.getItem('token');
    const authNav = document.getElementById('auth-nav');
    const profileNav = document.getElementById('profile-nav');
    const bookmarksNav = document.getElementById('bookmarks-nav');
    const logoutNav = document.getElementById('logout-nav');

    if (token) {
        // Пользователь авторизован
        if (authNav) authNav.classList.add('hidden');
        if (profileNav) profileNav.classList.remove('hidden');
        if (bookmarksNav) bookmarksNav.classList.remove('hidden');
        if (logoutNav) logoutNav.classList.remove('hidden');
    } else {
        // Пользователь не авторизован
        if (authNav) authNav.classList.remove('hidden');
        if (profileNav) profileNav.classList.add('hidden');
        if (bookmarksNav) bookmarksNav.classList.add('hidden');
        if (logoutNav) logoutNav.classList.add('hidden');
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/';
}

// Проверка статуса при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    checkAuthStatus();
});

// ========== API Helper Functions ==========

async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('token');
    
    const headers = options.headers || {};
    if (token && !headers['Authorization']) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
        ...options,
        headers: headers
    });

    if (response.status === 401) {
        // Токен истек или невалиден
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
    }

    return response;
}

// ========== Error Handling ==========

function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
    }
}

function showSuccess(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.style.display = 'block';
        setTimeout(() => {
            element.style.display = 'none';
        }, 3000);
    }
}

// ========== Utility Functions ==========

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatRating(rating) {
    return rating ? rating.toFixed(1) : '0.0';
}

function generateStars(rating) {
    const fullStars = Math.round(rating);
    const emptyStars = 5 - fullStars;
    return '★'.repeat(fullStars) + '☆'.repeat(emptyStars);
}

// ========== Local Storage Helpers ==========

function getUser() {
    const userJson = localStorage.getItem('user');
    return userJson ? JSON.parse(userJson) : null;
}

function setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
}

function isAuthenticated() {
    return !!localStorage.getItem('token');
}

// ========== Form Helpers ==========

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateUsername(username) {
    return username && username.length >= 3 && username.length <= 50;
}

function validatePassword(password) {
    return password && password.length >= 6;
}

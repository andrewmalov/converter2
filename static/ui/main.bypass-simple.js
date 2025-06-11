
/**
 * Упрощенная версия main.js с полностью отключенной авторизацией
 * Этот файл заменяет оригинальный main.js для работы без авторизации
 */

console.log('🔓 Загружается упрощенная версия main.js без авторизации');

// Глобальные настройки
window.authDisabled = true;
window.demoMode = true;
window.bypassAuth = true;
window.offlineMode = true;
window.isAuthenticated = true;
window.authenticated = true;
window.userRole = 'admin';
window.authToken = 'fake-jwt-token-12345';

// Данные пользователя
window.currentUser = {
    username: 'admin',
    role: 'admin',
    permissions: ['read', 'write', 'admin'],
    authenticated: true,
    id: 1,
    email: 'admin@localhost'
};

// Сохраняем в localStorage
localStorage.setItem('authToken', 'fake-jwt-token-12345');
localStorage.setItem('user', JSON.stringify(window.currentUser));
localStorage.setItem('isAuthenticated', 'true');

// Функции-заглушки для авторизации
window.login = function() { return Promise.resolve(window.currentUser); };
window.logout = function() { return Promise.resolve(); };
window.checkAuth = function() { return Promise.resolve(true); };
window.isLoggedIn = function() { return true; };
window.hasPermission = function() { return true; };
window.isAdmin = function() { return true; };

// Перехватываем Angular bootstrap если он есть
if (typeof ng !== 'undefined') {
    console.log('🅰️ Angular обнаружен, применяем патчи авторизации');
}

// Эмулируем успешную инициализацию приложения
document.addEventListener('DOMContentLoaded', function() {
    console.log('📱 Приложение инициализировано без авторизации');
    
    // Эмулируем событие успешной авторизации
    const authEvent = new CustomEvent('authSuccess', {
        detail: {
            user: window.currentUser,
            token: 'fake-jwt-token-12345'
        }
    });
    document.dispatchEvent(authEvent);
    
    // Скрываем элементы авторизации
    setTimeout(function() {
        const authElements = document.querySelectorAll('[class*="login"], [class*="auth"], [id*="login"], [id*="auth"]');
        authElements.forEach(el => {
            if (el.style) {
                el.style.display = 'none';
            }
        });
        
        // Показываем основной контент
        const appRoot = document.querySelector('app-root');
        if (appRoot) {
            appRoot.style.display = 'block';
        }
    }, 1000);
});

console.log('✅ Упрощенная версия main.js загружена успешно');

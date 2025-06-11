/**
 * Скрипт для полного отключения авторизации в Firewall Migration Tool
 * Этот файл перехватывает все HTTP запросы и отключает проверки авторизации
 */

console.log('🔓 Авторизация отключена - Auth Bypass активирован');

// Глобальные флаги для отключения авторизации
window.authDisabled = true;
window.demoMode = true;
window.bypassAuth = true;

// Перехватываем XMLHttpRequest
(function() {
    const originalXHR = window.XMLHttpRequest;
    const originalOpen = originalXHR.prototype.open;
    const originalSend = originalXHR.prototype.send;
    const originalSetRequestHeader = originalXHR.prototype.setRequestHeader;

    // Перехватываем open метод
    originalXHR.prototype.open = function(method, url, async, user, password) {
        this._method = method;
        this._url = url;
        console.log(`🌐 XHR Request: ${method} ${url}`);
        
        // Если это запрос к API авторизации, перенаправляем на наш прокси
        if (url.includes('/api/auth') || url.includes('/login') || url.includes('/authenticate')) {
            console.log('🔄 Перенаправление запроса авторизации на прокси');
            url = url.replace(/^.*\/api\//, '/api/');
        }
        
        return originalOpen.call(this, method, url, async, user, password);
    };

    // Перехватываем setRequestHeader для удаления заголовков авторизации
    originalXHR.prototype.setRequestHeader = function(header, value) {
        // Пропускаем заголовки авторизации
        if (header.toLowerCase().includes('authorization') || 
            header.toLowerCase().includes('x-auth') ||
            header.toLowerCase().includes('bearer')) {
            console.log(`🚫 Заблокирован заголовок авторизации: ${header}`);
            return;
        }
        return originalSetRequestHeader.call(this, header, value);
    };

    // Перехватываем send метод
    originalXHR.prototype.send = function(data) {
        const xhr = this;
        
        // Добавляем обработчик ответа
        const originalOnReadyStateChange = xhr.onreadystatechange;
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                // Если это запрос авторизации, возвращаем успешный ответ
                if (xhr._url && (xhr._url.includes('/api/auth') || 
                                xhr._url.includes('/login') || 
                                xhr._url.includes('/authenticate'))) {
                    console.log('✅ Имитация успешной авторизации');
                    
                    // Создаем успешный ответ
                    Object.defineProperty(xhr, 'status', { value: 200, writable: false });
                    Object.defineProperty(xhr, 'statusText', { value: 'OK', writable: false });
                    Object.defineProperty(xhr, 'responseText', { 
                        value: JSON.stringify({
                            status: 'success',
                            message: 'Authentication bypassed',
                            token: 'fake-jwt-token-12345',
                            user: {
                                username: 'admin',
                                role: 'admin',
                                permissions: ['read', 'write', 'admin']
                            },
                            authenticated: true
                        }), 
                        writable: false 
                    });
                }
            }
            
            if (originalOnReadyStateChange) {
                originalOnReadyStateChange.call(xhr);
            }
        };
        
        return originalSend.call(this, data);
    };
})();

// Перехватываем fetch API
(function() {
    const originalFetch = window.fetch;
    
    window.fetch = function(url, options = {}) {
        console.log(`🌐 Fetch Request: ${options.method || 'GET'} ${url}`);
        
        // Удаляем заголовки авторизации
        if (options.headers) {
            const headers = new Headers(options.headers);
            for (const [key, value] of headers.entries()) {
                if (key.toLowerCase().includes('authorization') || 
                    key.toLowerCase().includes('x-auth') ||
                    key.toLowerCase().includes('bearer')) {
                    console.log(`🚫 Удален заголовок авторизации: ${key}`);
                    headers.delete(key);
                }
            }
            options.headers = headers;
        }
        
        // Если это запрос авторизации, возвращаем успешный ответ
        if (url.includes('/api/auth') || url.includes('/login') || url.includes('/authenticate')) {
            console.log('✅ Имитация успешного fetch авторизации');
            return Promise.resolve(new Response(JSON.stringify({
                status: 'success',
                message: 'Authentication bypassed',
                token: 'fake-jwt-token-12345',
                user: {
                    username: 'admin',
                    role: 'admin',
                    permissions: ['read', 'write', 'admin']
                },
                authenticated: true
            }), {
                status: 200,
                statusText: 'OK',
                headers: { 'Content-Type': 'application/json' }
            }));
        }
        
        return originalFetch.call(this, url, options);
    };
})();

// Перехватываем localStorage для сохранения токенов
(function() {
    const originalSetItem = localStorage.setItem;
    const originalGetItem = localStorage.getItem;
    
    localStorage.setItem = function(key, value) {
        if (key.includes('token') || key.includes('auth') || key.includes('user')) {
            console.log(`💾 Сохранение в localStorage: ${key}`);
        }
        return originalSetItem.call(this, key, value);
    };
    
    localStorage.getItem = function(key) {
        if (key.includes('token') || key.includes('auth')) {
            console.log(`📖 Чтение токена из localStorage: ${key}`);
            // Возвращаем фейковый токен если его нет
            const value = originalGetItem.call(this, key);
            if (!value && key.includes('token')) {
                console.log('🔑 Возвращаем фейковый токен');
                return 'fake-jwt-token-12345';
            }
            return value;
        }
        return originalGetItem.call(this, key);
    };
})();

// Устанавливаем фейковые данные пользователя
localStorage.setItem('authToken', 'fake-jwt-token-12345');
localStorage.setItem('user', JSON.stringify({
    username: 'admin',
    role: 'admin',
    permissions: ['read', 'write', 'admin'],
    authenticated: true
}));

// Перехватываем проверки авторизации в Angular
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM загружен, применяем патчи авторизации');
    
    // Ждем загрузки Angular и применяем патчи
    setTimeout(function() {
        // Перехватываем Angular HTTP клиент если он доступен
        if (window.ng && window.ng.core) {
            console.log('🅰️ Angular обнаружен, применяем патчи');
        }
        
        // Устанавливаем глобальные переменные для Angular
        window.isAuthenticated = true;
        window.currentUser = {
            username: 'admin',
            role: 'admin',
            permissions: ['read', 'write', 'admin']
        };
        
        // Эмулируем успешную авторизацию
        const authEvent = new CustomEvent('authSuccess', {
            detail: {
                user: window.currentUser,
                token: 'fake-jwt-token-12345'
            }
        });
        document.dispatchEvent(authEvent);
        
    }, 1000);
});

// Перехватываем ошибки авторизации
window.addEventListener('error', function(event) {
    if (event.message && (event.message.includes('auth') || 
                         event.message.includes('unauthorized') ||
                         event.message.includes('403') ||
                         event.message.includes('401'))) {
        console.log('🛡️ Перехвачена ошибка авторизации:', event.message);
        event.preventDefault();
        return false;
    }
});

// Функция для принудительного обхода любых проверок авторизации
window.forceBypassAuth = function() {
    console.log('🔓 Принудительный обход авторизации активирован');
    
    // Устанавливаем все возможные флаги
    window.authenticated = true;
    window.isLoggedIn = true;
    window.authToken = 'fake-jwt-token-12345';
    window.userRole = 'admin';
    
    // Очищаем все таймеры авторизации
    for (let i = 1; i < 99999; i++) {
        window.clearTimeout(i);
        window.clearInterval(i);
    }
    
    // Эмулируем событие успешной авторизации
    const events = ['login', 'auth-success', 'user-authenticated', 'session-valid'];
    events.forEach(eventName => {
        const event = new CustomEvent(eventName, {
            detail: { 
                success: true, 
                user: window.currentUser,
                token: 'fake-jwt-token-12345'
            }
        });
        document.dispatchEvent(event);
        window.dispatchEvent(event);
    });
};

// Автоматически вызываем принудительный обход через 2 секунды
setTimeout(window.forceBypassAuth, 2000);

console.log('✅ Auth Bypass полностью активирован!');
console.log('🔧 Доступные команды:');
console.log('   - window.forceBypassAuth() - принудительный обход авторизации');
console.log('   - window.authDisabled - флаг отключения авторизации');
console.log('   - window.currentUser - данные текущего пользователя');
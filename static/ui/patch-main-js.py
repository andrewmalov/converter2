#!/usr/bin/env python3
"""
Скрипт для патчинга main.original.js для отключения авторизации
"""

import re
import os
import shutil

def patch_main_js():
    """Патчит main.original.js для отключения авторизации"""
    
    original_file = '/workspace/converter2/static/ui/main.original.js'
    patched_file = '/workspace/converter2/static/ui/main.patched.js'
    
    print("🔧 Начинаем патчинг main.original.js...")
    
    try:
        # Читаем оригинальный файл
        with open(original_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        print(f"📄 Размер оригинального файла: {len(content)} символов")
        
        # Список паттернов для замены
        patches = [
            # Отключаем проверки авторизации
            (r'\.setRequestHeader\s*\(\s*["\']Authorization["\']', '.setRequestHeader("X-Disabled-Authorization"'),
            (r'\.setRequestHeader\s*\(\s*["\']X-Auth["\']', '.setRequestHeader("X-Disabled-Auth"'),
            (r'\.setRequestHeader\s*\(\s*["\']Bearer["\']', '.setRequestHeader("X-Disabled-Bearer"'),
            
            # Заменяем проверки статуса 401/403
            (r'\.status\s*===?\s*401', '.status === 200'),
            (r'\.status\s*===?\s*403', '.status === 200'),
            (r'\.status\s*==\s*401', '.status == 200'),
            (r'\.status\s*==\s*403', '.status == 200'),
            
            # Отключаем редиректы на страницы авторизации
            (r'["\']\/login["\']', '"/demo"'),
            (r'["\']\/auth["\']', '"/demo"'),
            (r'["\']\/signin["\']', '"/demo"'),
            
            # Заменяем проверки токенов
            (r'!.*token', 'true || !token'),
            (r'token\s*===?\s*null', 'false'),
            (r'token\s*===?\s*undefined', 'false'),
            (r'!.*authenticated', 'false'),
            
            # Отключаем таймауты сессии
            (r'sessionTimeout', 'disabledSessionTimeout'),
            (r'authTimeout', 'disabledAuthTimeout'),
            
            # Заменяем проверки ролей
            (r'role\s*!==?\s*["\']admin["\']', 'false'),
            (r'!.*isAdmin', 'false'),
            (r'!.*hasPermission', 'false'),
        ]
        
        # Применяем патчи
        patched_content = content
        patches_applied = 0
        
        for pattern, replacement in patches:
            matches = len(re.findall(pattern, patched_content, re.IGNORECASE))
            if matches > 0:
                patched_content = re.sub(pattern, replacement, patched_content, flags=re.IGNORECASE)
                patches_applied += matches
                print(f"✅ Применен патч: {pattern} -> {replacement} ({matches} замен)")
        
        # Добавляем код для принудительного отключения авторизации в начало файла
        auth_bypass_code = '''
// === AUTH BYPASS PATCH ===
window.authDisabled = true;
window.demoMode = true;
window.bypassAuth = true;
window.isAuthenticated = true;
window.currentUser = {username: 'admin', role: 'admin', permissions: ['read', 'write', 'admin']};
console.log('🔓 Auth bypass патч активирован в main.js');
// === END AUTH BYPASS PATCH ===

'''
        
        patched_content = auth_bypass_code + patched_content
        
        # Сохраняем патченый файл
        with open(patched_file, 'w', encoding='utf-8') as f:
            f.write(patched_content)
        
        print(f"✅ Патчинг завершен!")
        print(f"📊 Применено {patches_applied} патчей")
        print(f"💾 Патченый файл сохранен как: {patched_file}")
        print(f"📄 Размер патченого файла: {len(patched_content)} символов")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при патчинге: {e}")
        return False

def create_bypass_main_js():
    """Создает упрощенную версию main.js с отключенной авторизацией"""
    
    bypass_file = '/workspace/converter2/static/ui/main.bypass-simple.js'
    
    bypass_content = '''
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
'''
    
    try:
        with open(bypass_file, 'w', encoding='utf-8') as f:
            f.write(bypass_content)
        print(f"✅ Создана упрощенная версия: {bypass_file}")
        return True
    except Exception as e:
        print(f"❌ Ошибка при создании упрощенной версии: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Запуск патчера для отключения авторизации")
    print("=" * 50)
    
    # Создаем упрощенную версию
    create_bypass_main_js()
    
    # Патчим оригинальный файл
    patch_main_js()
    
    print("=" * 50)
    print("✅ Патчинг завершен!")
    print("📋 Доступные файлы:")
    print("   - main.original.js (оригинал)")
    print("   - main.patched.js (патченая версия)")
    print("   - main.bypass-simple.js (упрощенная версия)")
    print("   - main.bypass.js (существующая версия)")
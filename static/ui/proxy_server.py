#!/usr/bin/env python3
"""
Простой прокси-сервер для обхода авторизации в Firewall Migration Tool
"""

import http.server
import socketserver
import urllib.request
import urllib.parse
import json
import os
from urllib.parse import urlparse, parse_qs

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Загружаем финальную версию приложения с полностью отключенной авторизацией
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index_final.html'
        
        # Доступ к версии без авторизации через /noauth
        elif self.path == '/noauth':
            self.path = '/index_no_auth.html'
        
        # Доступ к рабочей версии через /working
        elif self.path == '/working':
            self.path = '/working.html'
        
        # Доступ к демо-странице через /demo
        elif self.path == '/demo':
            self.path = '/bypass.html'
        
        # Доступ к оригинальному приложению через /original
        elif self.path == '/original':
            self.path = '/index.html'
        
        # Обработка запроса EULA
        elif self.path == '/api/eula_check':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # Возвращаем успешный ответ для EULA
            response = {
                "status": "success",
                "eula_accepted": True,
                "message": "EULA check bypassed"
            }
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Обработка других API запросов - возвращаем успешные ответы
        elif self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "success", "message": "API call bypassed"}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # Для всех остальных запросов используем стандартную обработку
        super().do_GET()
    
    def do_POST(self):
        # Обработка POST запросов к API
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Специальная обработка для логина
            if self.path == '/api/auth/login':
                response = {
                    "status": "success",
                    "message": "Login successful",
                    "token": "fake-jwt-token-12345",
                    "user": {
                        "username": "admin",
                        "role": "admin",
                        "permissions": ["read", "write", "admin"]
                    },
                    "authenticated": True
                }
            else:
                response = {"status": "success", "message": "API POST bypassed"}
            
            self.wfile.write(json.dumps(response).encode())
            return
        
        super().do_POST()
    
    def do_OPTIONS(self):
        # Обработка CORS preflight запросов
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == "__main__":
    PORT = 12001
    
    # Переходим в директорию с файлами приложения
    #os.chdir('/workspace/converter')
    
    with socketserver.TCPServer(("0.0.0.0", PORT), ProxyHandler) as httpd:
        print(f"🚀 Сервер запущен на порту {PORT}")
        print(f"🌐 Приложение доступно по адресу: https://work-2-xrvofshduudwgugx.prod-runtime.all-hands.dev")
        print("🔓 Авторизация отключена - все API запросы будут возвращать успешные ответы")
        print("")
        print("📋 Доступные маршруты:")
        print("   / или /index.html    - Финальная версия с отключенной авторизацией")
        print("   /noauth             - Версия без авторизации")
        print("   /working            - Рабочая версия")
        print("   /demo               - Демо-страница")
        print("   /original           - Оригинальное приложение")
        print("")
        print("🔧 Для принудительного обхода авторизации выполните в консоли браузера:")
        print("   window.forceOfflineMode()")
        httpd.serve_forever()

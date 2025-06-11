#!/bin/bash

# 🚀 Скрипт для запуска Firewall Migration Tool в автономном режиме
# Авторизация полностью отключена

echo "🔓 Firewall Migration Tool - Автономный режим"
echo "=============================================="

# Переходим в директорию с приложением
cd /workspace/converter2/static/ui

# Проверяем наличие необходимых файлов
echo "📋 Проверка файлов..."

required_files=(
    "auth-bypass.js"
    "index_final.html" 
    "main.patched.js"
    "proxy_server.py"
)

missing_files=()
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        missing_files+=("$file")
    fi
done

if [[ ${#missing_files[@]} -gt 0 ]]; then
    echo "❌ Отсутствуют файлы:"
    printf '   - %s\n' "${missing_files[@]}"
    echo ""
    echo "🔧 Запустите патчер для создания недостающих файлов:"
    echo "   python3 patch-main-js.py"
    exit 1
fi

echo "✅ Все файлы найдены"

# Останавливаем существующие процессы
echo "🛑 Остановка существующих серверов..."
pkill -f proxy_server.py 2>/dev/null || true

# Ждем завершения процессов
sleep 2

# Запускаем сервер
echo "🚀 Запуск сервера..."
python3 proxy_server.py &
SERVER_PID=$!

# Ждем запуска сервера
sleep 3

# Проверяем, что сервер запустился
if kill -0 $SERVER_PID 2>/dev/null; then
    echo ""
    echo "✅ Сервер успешно запущен!"
    echo ""
    echo "🌐 Приложение доступно по адресам:"
    echo "   https://work-2-xrvofshduudwgugx.prod-runtime.all-hands.dev"
    echo "   (порт 12001)"
    echo ""
    echo "📋 Доступные маршруты:"
    echo "   /                    - Финальная версия (рекомендуется)"
    echo "   /noauth             - Версия без авторизации"
    echo "   /working            - Рабочая версия"
    echo "   /demo               - Демо-страница"
    echo "   /original           - Оригинальное приложение"
    echo ""
    echo "🔧 Команды для консоли браузера:"
    echo "   window.forceOfflineMode()    - Принудительный обход авторизации"
    echo "   window.authDisabled          - Проверка статуса авторизации"
    echo ""
    echo "🛑 Для остановки сервера:"
    echo "   pkill -f proxy_server.py"
    echo ""
    echo "📄 Подробная документация: README_AUTH_BYPASS.md"
    echo ""
    echo "🔓 Авторизация отключена - приложение готово к работе!"
else
    echo "❌ Ошибка запуска сервера"
    exit 1
fi
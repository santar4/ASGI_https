# Проект: Чат із використанням WebSocket та FastAPI

## Опис
Цей проект реалізує простий чат із використанням **FastAPI** та **WebSocket**. Також включені можливості компресії відповідей, HTTPS-перенаправлення, і використання довірених хостів для забезпечення безпеки. Для відображення HTML-сторінок використовується шаблонізатор Jinja2.

## Основні функції
1. **WebSocket:** підтримка двостороннього зв'язку між клієнтом та сервером.
2. **Компресія відповідей:** автоматична компресія великих відповідей (>1000 байтів).
3. **HTTPS-перенаправлення:** перенаправлення HTTP-запитів на HTTPS для підвищення безпеки.
4. **Довірені хости:** обмеження доступу до API тільки для дозволених доменів.
5. **Демонстрація шаблонів Jinja2:** HTML-сторінка для тестування WebSocket.

## Встановлення
1. **Клонувати репозиторій:**
   ```bash
   git clone https://github.com/username/repository_name.git
   ```

## Запуск проекту
Для запуску використовується модуль `server_run`:
```bash
python main.py
```

## Структура проекту
- **main.py:** Головний файл програми.
- **templates/**: Папка для HTML-шаблонів.
- **tools.py:** Файл із функціями компресії (приклад функції `compress_response`).
- **server_run.py:** Модуль для запуску сервера (uvicorn/hypercorn).

## Доступні маршрути
- **`GET /`**: Повертає HTML-сторінку WebSocket-клієнта.
- **`GET /large_text`**: Генерує великий текст для тестування компресії.
- **`GET /hello`**: Привітання користувача (асинхронно).
- **`/ws/base`**: WebSocket-з'єднання для чату.

## Мідлвейр
- **HTTPSRedirectMiddleware:** Перенаправляє всі HTTP-запити на HTTPS.
- **GZipMiddleware:** Компресує відповіді, якщо їх розмір перевищує 1000 байтів.
- **TrustedHostMiddleware:** Дозволяє запити лише від визначених хостів (`www.example.com`, `example.com`, `127.0.0.1`).

## Вимоги
- Python 3.9+
- FastAPI
- Starlette
- Jinja2
- Uvicorn

## Приклад роботи WebSocket
1. Підключення до WebSocket: `ws://127.0.0.1:8000/ws/base`
2. Надсилання повідомлення: `{"message": "Привіт"}`
3. Отримання відповіді від сервера: `Server get message: Привіт`

## Ліцензія
Цей проект розповсюджується під ліцензією MIT.


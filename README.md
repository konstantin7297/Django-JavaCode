# Описание:
Небольшое приложение в виде REST API представляет всего 2 endpoint'а для запросов:
- http://127.0.0.1:8000/api/v1/wallet/ - POST запрос для создания операции.
- http://127.0.0.1:8000/api/v1/wallets/<WALLET_UUID>/ - GET запрос для получения информации.
## Работа с проектом:
1. **[Опционально]** Установка переменных окружения в файле `.env`.
2. Сборка проекта командой: `docker-compose build`.
3. Запуск проекта командой: `docker-compose up -d`.
4. Выключение проекта командой: `docker-compose down`.
## Дополнительно:
1. Генерация тестовых кошельков: `docker exec server-1 python manage.py create_wallets`.
2. Ручной запуск тестов: `docker exec server-1 python manage.py test wallets`.
## Основные технологии: 
- Python 3.10
- Django 5.1.1
- Django REST Framework 3.15.2
- База данных PostgreSQL 13:15
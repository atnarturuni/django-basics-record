# Time Tracker

Проект-пример для демонстрации возможностей Django на онлайн курсе для Казанского федерального университета.

## Запуск проекта для разработки

- `python3 -m venv venv` - создание виртуального окружения
- `source venv/bin/activate` - войти в виртуальное окружение
- `pip install -r requirements.txt` - установка зависимостей
- `docker-compose up -d` - запустить дополнительные сервисы в Docker. Если у Вас нет Docker, установите
  - [PostgreSQL](https://www.postgresql.org/)
- `python manage.py migrate` - примененить миграции
- `python manage.py runserver` - запустить сервер для разработки на http://127.0.0.1:8000

&copy; 2023 [Артур Атнагулов](https://atnartur.dev)

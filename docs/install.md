# Установка и запуск

## Требования

- Python 3.11+
- pip
- Git

## Клонирование репозитория

```bash
git clone https://github.com/vladimirperov85/Django-PC-Shop.git
cd PC_Shop
Виртуальное окружение
Изоляция зависимостей проекта от системного Python:

bash
# Создание
python -m venv .venv

# Активация (Windows)
.venv\Scripts\activate

# Активация (Linux/macOS)
source .venv/bin/activate
Зависимости
bash
pip install -r requirements.txt
Основные зависимости: Django 5.2, Pillow (изображения), psycopg2-binary (PostgreSQL), python-decouple (конфигурация из .env).

Переменные окружения
Секреты проекта хранятся в файле .env, который не попадает в git. Шаблон — в .env.example:

bash
cp .env.example .env
Минимум для локального запуска:

env
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
По умолчанию проект использует SQLite — база создаётся автоматически.

Миграции и суперпользователь
bash
python manage.py migrate
python manage.py createsuperuser
Запуск
bash
python manage.py runserver
Сайт: `http://127.0.0.1:8000/` · Админка: `http://127.0.0.1:8000/admin/`

Продакшен-конфигурация
Проект поддерживает две СУБД — выбор задаётся переменой DB_ENGINE в .env:

Параметр	Разработка	Продакшен
СУБД	SQLite	PostgreSQL (DB_ENGINE=postgres)
DEBUG	True	False
Запуск	runserver	Gunicorn + Nginx
Для PostgreSQL в .env дополнительно указываются DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.

Тесты
bash
python manage.py test shop
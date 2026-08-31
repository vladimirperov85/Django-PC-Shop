# ⚙️ COMMANDS — Часто используемые команды проекта PC_Shop

> Справочник команд для работы с проектом: локально (Windows) и на сервере (Ubuntu).
> Локально — команды выполняются в терминале на вашем ПК.
> Сервер — команды выполняются по SSH на `root@139.100.238.148`.

---

## 📁 Виртуальное окружение

### Локально (Windows)
```bash
# Создать окружение
python -m venv .venv

# Активировать
.venv\Scripts\activate

# Деактивировать
deactivate
```

### Сервер (Ubuntu)
```bash
# Создать окружение
python3 -m venv .venv

# Активировать
source .venv/bin/activate

# Деактивировать
deactivate
```

---

## 🐍 Django

```bash
# Запустить dev-сервер (локально)
python manage.py runserver

# Применить миграции
python manage.py migrate

# Создать миграции после изменения моделей
python manage.py makemigrations

# Собрать статику
python manage.py collectstatic --noinput

# Создать суперпользователя
python manage.py createsuperuser

# Проверка безопасности для продакшена
python manage.py check --deploy

# Выгрузить данные (fixture)
python manage.py dumpdata --natural-foreign --natural-primary -o data.json

# Загрузить данные (fixture)
python manage.py loaddata data.json

# Открыть shell
python manage.py shell
```

---

## 🧪 Тесты

> ⚠️ **Важно:** перед запуском тестов активируй виртуальное окружение (см. раздел «Виртуальное окружение»).
> Тесты запускаются **только** через `manage.py`, а не напрямую (`python tests.py` — так не работает).

### Локально (Windows)
```bash
# Активировать окружение (если ещё не активировано)
.venv\Scripts\activate

# Запустить ВСЕ тесты проекта
python manage.py test

# Запустить тесты конкретного приложения (например, shop)
python manage.py test shop

# Запустить тесты конкретного класса (например, OrderItemModelTest)
python manage.py test shop.tests.OrderItemModelTest

# Запустить один конкретный тест (метод)
python manage.py test shop.tests.OrderItemModelTest.test_get_cost_calculates_price_times_quantity

# Запустить с подробным выводом (уровень детализации 2)
python manage.py test shop -v 2
```

### Сервер (Ubuntu)
```bash
# Активировать окружение
source .venv/bin/activate

# Запустить тесты
python manage.py test shop
```

> **Как читать вывод:**
> - `.` (точка) — тест прошёл успешно
> - `F` — тест упал (проверка не совпала)
> - `E` — ошибка в самом тесте
> - `OK` в конце — все тесты прошли

---

## 🔄 Git

```bash
# Посмотреть статус
git status

# Добавить все изменения
git add -A

# Закоммитить
git commit -m "Сообщение"

# Отправить на GitHub
git push origin main

# Скачать с GitHub (на сервере)
git pull origin main

# Посмотреть историю коммитов
git log --oneline
```

---

## 🖥️ Сервер (SSH)

```bash
# Подключиться к серверу
ssh root@139.100.238.148

# Выйти
exit
```

---

## 🚀 Gunicorn (systemd-сервис)

```bash
# Статус
sudo systemctl status gunicorn

# Перезапуск (после изменений кода/.env)
sudo systemctl restart gunicorn

# Перезагрузка на лету (HUP, без остановки)
sudo systemctl reload gunicorn

# Логи в реальном времени
sudo journalctl -u gunicorn -f

# Последние N строк логов
sudo journalctl -u gunicorn -n 50
```

---

## 🌐 Nginx

```bash
# Статус
sudo systemctl status nginx

# Проверить конфиг (безопасно, не применяет)
sudo nginx -t

# Применить конфиг без остановки
sudo systemctl reload nginx

# Перезапустить
sudo systemctl restart nginx

# Логи ошибок
sudo tail /var/log/nginx/error.log
```

---

## 🗄️ PostgreSQL

```bash
# Статус
sudo systemctl status postgresql

# Проверить, что принимает подключения
pg_isready

# Войти в консоль PostgreSQL (под postgres)
sudo -u postgres psql

# Выполнить SQL-команду без входа в консоль
sudo -u postgres psql -c "SQL-команда"

# Сменить пароль пользователя
sudo -u postgres psql -c "ALTER USER shop_user WITH PASSWORD 'новый_пароль';"
```

---

## 🔥 Файрвол UFW

```bash
# Статус
sudo ufw status verbose

# Открыть порт
sudo ufw allow 80/tcp

# Закрыть порт
sudo ufw delete allow 8000/tcp
```

---

## 🔄 Цикл обновления проекта (на сервере)

```bash
cd /root/PC_Shop
source .venv/bin/activate

git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

> Подробнее о том, какие шаги нужны в зависимости от изменений — в файле `UPDATE CYCLE.md`.

---

## 🧪 Полезные проверки

```bash
# Версия Django
python -c "import django; print(django.get_version())"

# Проверка подключения к БД
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('DB connection OK')"

# Проверить HTTP-ответ (заголовки) без браузера
curl -I http://139.100.238.148
```

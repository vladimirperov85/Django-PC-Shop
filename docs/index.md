# PC_Shop

PC_Shop — интернет-магазин компьютерной техники
Веб-приложение на Django: каталог сборок ПК, корзина, оформление заказов
и личный кабинет покупателя.

<div class="grid cards" markdown>

:material-monitor: Каталог товаров
--

Категории, поиск по названию, пагинация, карточки товаров с изображениями.
:material-cart-outline: Корзина на сессиях
Добавление через AJAX без перезагрузки страницы, счётчик в шапке сайта.
:material-package-variant-closed: Заказы
---
Оформление заказа, статусы (новый, оплачен, доставлен), история покупок.

:material-account: Пользователи
---
Регистрация, вход, личный кабинет с заказами.

</div>

Стек технологий
Python 3 / Django 5.2
SQLite (разработка) / PostgreSQL (продакшен, через конфигурацию)
Pillow — обработка изображений товаров
python-decouple — конфигурация через .env

Ссылки
[:fontawesome-brands-github: Исходный код на GitHub](https://github.com/vladimirperov85/Django-PC-Shop){ .md-button }
[:material-book-open-variant: Установка и запуск](install.md){ .md-button .md-button--primary }

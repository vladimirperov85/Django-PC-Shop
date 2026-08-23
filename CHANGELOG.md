# CHANGELOG

Все значимые изменения проекта документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование — [Semantic Versioning](https://semver.org/lang/ru/).

## [1.0.0] — 2026-08-23

### Добавлено
- Стиль ссылки «Главная» в хлебных крошках под тему сайта (цвет `#d9c2f0`)
- Рефакторинг `shop/urls.py` и `shop/views.py`

### Изменено
- `shop/static/shop/css/main.css` — добавлено правило `.breadcrumb-item a`
- `shop/urls.py`, `shop/views.py` — рефакторинг

### Исправлено
- Ссылка «Главная» в хлебных крошках отображалась стандартным синим цветом Bootstrap вместо фирменного фиолетового

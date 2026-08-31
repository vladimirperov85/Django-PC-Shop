from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase

from .forms import OrderForm, UserRegisterForm
from .models import Category, Order, OrderItem, Product


class OrderItemModelTest(TestCase):
    """Тесты для модели OrderItem."""

    def test_get_cost_calculates_price_times_quantity(self):
        """Стоимость позиции = цена × количество."""
        # 1. Подготовка: создаём данные
        category = Category.objects.create(name="Игровые", slug="gaming")
        product = Product.objects.create(
            category=category,
            name="Игровой ПК",
            slug="gaming-pc",
            price=100.00,
        )
        order = Order.objects.create(
            first_name="Иван",
            last_name="Петров",
            email="ivan@mail.ru",
            phone="+7991234567",
            address="Москва",
        )
        item = OrderItem.objects.create(
            order=order,
            product=product,
            price=100.00,
            quantity=3,
        )

        # 2. Проверка: вызываем метод и сравниваем с ожидаемым результатом
        self.assertEqual(item.get_cost(), Decimal("300.00"))


class OrderModelTest(TestCase):
    """Тесты для модели Order."""

    def test_get_total_cost_sums_all_items(self):
        """Общая стоимость заказа = сумма стоимостей всех позиций."""
        # 1. Подготовка: создаём категорию, товары и заказ
        category = Category.objects.create(name="Игровые", slug="gaming")
        pc = Product.objects.create(
            category=category, name="Игровой ПК", slug="gaming-pc", price=100.00
        )
        mouse = Product.objects.create(
            category=category, name="Мышка", slug="mouse", price=50.00
        )
        order = Order.objects.create(
            first_name="Иван",
            last_name="Петров",
            email="ivan@mail.ru",
            phone="+7991234567",
            address="Москва",
        )
        # 2. Добавляем в заказ две позиции
        OrderItem.objects.create(order=order, product=pc, price=100.00, quantity=2)
        OrderItem.objects.create(order=order, product=mouse, price=50.00, quantity=1)

        # 3. Проверка: 100×2 + 50×1 = 250
        self.assertEqual(order.get_total_cost(), Decimal("250.00"))


class GetAbsoluteUrlTest(TestCase):
    """Тесты для метода get_absolute_url() у Category и Product."""

    def setUp(self):
        """Общая подготовка: выполняется перед КАЖДЫМ тестом класса."""
        self.category = Category.objects.create(name="Игровые", slug="gaming")
        self.product = Product.objects.create(
            category=self.category,
            name="Игровой ПК",
            slug="gaming-pc",
            price=100.00,
        )

    def test_category_get_absolute_url(self):
        """URL категории строится по маршруту products_by_category."""
        self.assertEqual(self.category.get_absolute_url(), "/category/gaming/")

    def test_product_get_absolute_url(self):
        """URL товара строится по маршруту product_detail."""
        self.assertEqual(self.product.get_absolute_url(), "/product/gaming-pc/")


class StrRepresentationTest(TestCase):
    """Тесты для строкового представления моделей (__str__)."""

    def setUp(self):
        """Общая подготовка: выполняется перед КАЖДЫМ тестом класса."""
        self.category = Category.objects.create(name="Игровые", slug="gaming")
        self.product = Product.objects.create(
            category=self.category,
            name="Игровой ПК",
            slug="gaming-pc",
            price=100.00,
        )
        self.order = Order.objects.create(
            first_name="Иван",
            last_name="Петров",
            email="ivan@mail.ru",
            phone="+7991234567",
            address="Москва",
        )

    def test_category_str_returns_name(self):
        """Категория отображается своим названием."""
        self.assertEqual(str(self.category), "Игровые")

    def test_product_str_returns_name(self):
        """Товар отображается своим названием."""
        self.assertEqual(str(self.product), "Игровой ПК")

    def test_order_str_contains_id_and_last_name(self):
        """Заказ отображается как 'Заказ <id> от <фамилия>'."""
        self.assertEqual(str(self.order), f"Заказ {self.order.id} от Петров")

    def test_order_item_str_returns_id(self):
        """Позиция заказа отображается своим id."""
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=100.00,
            quantity=1,
        )
        self.assertEqual(str(item), str(item.id))


class OrderFormTest(TestCase):
    """Тесты для формы оформления заказа (OrderForm)."""

    def setUp(self):
        """Валидные данные, которые будем использовать в тестах."""
        self.valid_data = {
            "first_name": "Иван",
            "last_name": "Петров",
            "email": "ivan@mail.ru",
            "phone": "+7-999-123-45-67",
            "address": "г. Москва, ул. Ленина, д. 10",
        }

    def test_form_valid_with_correct_data(self):
        """Форма валидна при правильных данных."""
        form = OrderForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_empty_data(self):
        """Форма невалидна, если отправить пустые данные."""
        form = OrderForm(data={})
        self.assertFalse(form.is_valid())
        # Все 5 обязательных полей должны попасть в список ошибок
        self.assertEqual(len(form.errors), 5)

    def test_form_invalid_with_bad_email(self):
        """Форма невалидна, если email не похож на email."""
        bad_data = self.valid_data.copy()
        bad_data["email"] = "ivan@mail"  # нет доменной зоны
        form = OrderForm(data=bad_data)
        self.assertFalse(form.is_valid())
        # Ошибка должна быть именно в поле email
        self.assertIn("email", form.errors)


class UserRegisterFormTest(TestCase):
    """Тесты для формы регистрации пользователя (UserRegisterForm)."""

    def setUp(self):
        """Валидные данные для регистрации."""
        self.valid_data = {
            "username": "ivan2024",
            "email": "ivan@mail.ru",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }

    def test_form_valid_with_correct_data(self):
        """Форма валидна при правильных данных."""
        form = UserRegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_passwords_do_not_match(self):
        """Форма невалидна, если пароли не совпадают."""
        bad_data = self.valid_data.copy()
        bad_data["password2"] = "AnotherPass456!"
        form = UserRegisterForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_with_weak_password(self):
        """Форма невалидна, если пароль слишком простой."""
        bad_data = self.valid_data.copy()
        bad_data["password1"] = "123"
        bad_data["password2"] = "123"
        form = UserRegisterForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_without_email(self):
        """Форма невалидна, если email не заполнен (мы сделали его обязательным)."""
        bad_data = self.valid_data.copy()
        bad_data["email"] = ""
        form = UserRegisterForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class ProductPagesTest(TestCase):
    """Тесты для страниц товаров и категорий (простые GET-запросы)."""

    def setUp(self):
        """Общая подготовка: категория и товар в базе."""
        self.category = Category.objects.create(name="Игровые", slug="gaming")
        self.product = Product.objects.create(
            category=self.category,
            name="Игровой ПК",
            slug="gaming-pc",
            price=100.00,
            available=True,
        )

    def test_product_list_page_returns_200(self):
        """Главная страница со списком товаров открывается."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page_returns_200(self):
        """Страница существующего товара открывается."""
        response = self.client.get("/product/gaming-pc/")
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page_returns_404_for_missing_product(self):
        """Страница несуществующего товара даёт 404."""
        response = self.client.get("/product/no-such-pc/")
        self.assertEqual(response.status_code, 404)

    def test_category_page_returns_200(self):
        """Страница категории открывается."""
        response = self.client.get("/category/gaming/")
        self.assertEqual(response.status_code, 200)


class RegistrationAndAuthPagesTest(TestCase):
    """Тесты страниц регистрации, логина и защиты @login_required."""

    def test_register_page_returns_200(self):
        """Страница регистрации открывается."""
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)

    def test_register_post_creates_user_and_redirects(self):
        """POST с правильными данными создаёт пользователя и делает редирект."""
        data = {
            "username": "ivan2024",
            "email": "ivan@mail.ru",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        response = self.client.post("/register/", data=data)
        # 1. Пользователь реально создан в базе
        self.assertTrue(User.objects.filter(username="ivan2024").exists())
        # 2. Сервер перенаправил на главную (редирект = код 302)
        self.assertRedirects(response, "/")

    def test_my_orders_redirects_anonymous_to_login(self):
        """Анонимного пользователя 'Мои заказы' отправляет на логин."""
        response = self.client.get("/my-orders/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_login_page_returns_200(self):
        """Страница входа открывается."""
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)


class CartViewsTest(TestCase):
    """Тесты корзины: добавление, повторное добавление, удаление, страница."""

    def setUp(self):
        """Товар, с которым будем работать."""
        self.category = Category.objects.create(name="Игровые", slug="gaming")
        self.product = Product.objects.create(
            category=self.category,
            name="Игровой ПК",
            slug="gaming-pc",
            price=100.00,
            available=True,
        )

    def _get_cart(self):
        """Достать корзину из сессии тестового клиента."""
        session = self.client.session
        return session.get(settings.CART_SESSION_ID, {})

    def test_cart_add_redirects_and_saves_product(self):
        """Добавление товара: редирект на корзину + товар в сессии."""
        response = self.client.post(f"/cart/add/{self.product.id}/")
        self.assertRedirects(response, "/cart/")
        cart = self._get_cart()
        self.assertIn(str(self.product.id), cart)
        self.assertEqual(cart[str(self.product.id)]["quantity"], 1)

    def test_cart_add_twice_does_not_duplicate(self):
        """Повторное добавление того же товара не увеличивает количество."""
        self.client.post(f"/cart/add/{self.product.id}/")
        self.client.post(f"/cart/add/{self.product.id}/")
        cart = self._get_cart()
        # Товар в корзине один, количество осталось 1
        self.assertEqual(len(cart), 1)
        self.assertEqual(cart[str(self.product.id)]["quantity"], 1)

    def test_cart_remove_deletes_product(self):
        """Удаление товара очищает корзину."""
        self.client.post(f"/cart/add/{self.product.id}/")
        self.client.post(f"/cart/remove/{self.product.id}/")
        cart = self._get_cart()
        self.assertNotIn(str(self.product.id), cart)

    def test_cart_detail_page_returns_200(self):
        """Страница корзины открывается."""
        response = self.client.get("/cart/")
        self.assertEqual(response.status_code, 200)


class OrderCreateViewTest(TestCase):
    """Тесты оформления заказа: корзина + форма + создание записей в БД."""

    def setUp(self):
        """Категория, товар и данные для формы заказа."""
        self.category = Category.objects.create(name="Игровые", slug="gaming")
        self.product = Product.objects.create(
            category=self.category,
            name="Игровой ПК",
            slug="gaming-pc",
            price=100.00,
            available=True,
        )
        self.valid_data = {
            "first_name": "Иван",
            "last_name": "Петров",
            "email": "ivan@mail.ru",
            "phone": "+7-999-123-45-67",
            "address": "г. Москва, ул. Ленина, д. 10",
        }

    def _add_product_to_cart(self):
        """Кладём товар в корзину через вьюху (как это сделал бы пользователь)."""
        self.client.post(f"/cart/add/{self.product.id}/")

    def test_order_create_page_returns_200(self):
        """Страница оформления заказа открывается."""
        response = self.client.get("/order/create/")
        self.assertEqual(response.status_code, 200)

    def test_order_create_post_creates_order_and_clears_cart(self):
        """POST с данными создаёт заказ и позицию, очищает корзину."""
        self._add_product_to_cart()
        response = self.client.post("/order/create/", data=self.valid_data)

        # 1. Редирект на страницу подтверждения
        self.assertRedirects(response, "/order/created/")

        # 2. Заказ создан ровно один, с данными из формы
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.first_name, "Иван")
        self.assertEqual(order.email, "ivan@mail.ru")

        # 3. Позиция заказа создана с ценой и количеством из корзины
        item = OrderItem.objects.get(order=order)
        self.assertEqual(item.product, self.product)
        self.assertEqual(item.price, Decimal("100.00"))
        self.assertEqual(item.quantity, 1)

        # 4. Корзина после заказа пуста
        cart = self.client.session.get(settings.CART_SESSION_ID, {})
        self.assertEqual(cart, {})

    def test_order_create_post_invalid_data_does_not_create_order(self):
        """POST с пустыми данными не создаёт заказ, форма возвращается с ошибками."""
        response = self.client.post("/order/create/", data={})
        self.assertEqual(response.status_code, 200)  # страница вернулась с ошибками
        self.assertEqual(Order.objects.count(), 0)  # заказ НЕ создан

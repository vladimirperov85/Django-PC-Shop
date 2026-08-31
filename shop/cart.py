from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    """Корзина покупок, хранящаяся в сессии пользователя."""

    def __init__(self, request):
        """
        Инициализируем корзину.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем пустую корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Добавить товар в корзину или обновить его количество.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как изменённую, чтобы Django сохранила её
        self.session.modified = True

    def remove(self, product):
        """
        Удалить товар из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def has_product(self, product):
        """Проверить, есть ли товар уже в корзине."""
        return str(product.id) in self.cart

    def __iter__(self):
        """
        Перебираем товары в корзине и получаем объекты Product из БД.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        Считаем общее количество товаров в корзине.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        """
        Считаем общую стоимость корзины.
        """
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        """
        Полностью очищаем корзину (будет использоваться при оформлении заказа).
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

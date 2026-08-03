from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    """Категории товаров: Игровые, Офисные и т.д."""

    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name="URL-идентификатор"
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_by_category", args=[self.slug])


class Product(models.Model):
    """Товары (сборки ПК)"""

    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(
        max_length=200, db_index=True, verbose_name="URL-идентификатор"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="products/%Y/%m/%d", blank=True, null=True, verbose_name="Изображение"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    available = models.BooleanField(default=True, verbose_name="В наличии")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлён")

    class Meta:
        ordering = ["name"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=["id", "slug"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])


class Order(models.Model):
    """Заказ покупателя."""

    STATUS_NEW = "new"
    STATUS_PROCESSING = "processing"
    STATUS_PAID = "paid"
    STATUS_DELIVERED = "delivered"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_NEW, "Новый"),
        (STATUS_PROCESSING, "Обрабатывается"),
        (STATUS_PAID, "Оплачен"),
        (STATUS_DELIVERED, "Доставлен"),
        (STATUS_CANCELLED, "Отменён"),
    ]

    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=20)
    address = models.CharField("Адрес", max_length=200)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    updated = models.DateTimeField("Дата обновления", auto_now=True)
    paid = models.BooleanField("Оплачен", default=False)
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
    )

    user = models.ForeignKey(
        User,
        related_name="orders",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Заказ {self.id} от {self.last_name}"

    def get_total_cost(self):
        """Общая стоимость заказа."""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Товар внутри заказа."""

    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        """Стоимость позиции (цена × количество)."""
        return self.price * self.quantity

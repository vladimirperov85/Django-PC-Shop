# PC_Shop/shop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Product
from .models import Category, Order, OrderItem
from .cart import Cart
from .forms import OrderForm, UserRegisterForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages


def product_list(request):
    """
    View для отображения списка всех товаров.
    Товары разбиты на страницы — по 10 штук на каждой.
    Поддерживает поиск по названию через параметр ?q=...
    """
    # Достаём из БД все товары, которые есть в наличии (available=True)
    products = Product.objects.filter(available=True).order_by("name")

    # Если в GET-запросе есть параметр ?q=... — фильтруем по названию
    query = request.GET.get("q")
    if query:
        products = products.filter(name__icontains=query)

    # Paginator разбивает queryset на страницы по 10 товаров
    paginator = Paginator(products, 9)

    # Номер страницы берём из GET-параметра ?page=2 (по умолчанию — 1)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # Передаём query в шаблон, чтобы сохранить текст в поле поиска
    # и search_params — для ссылок пагинации (чтобы не терять ?q=)
    search_params = ""
    if query:
        search_params = f"q={query}&"

    return render(
        request,
        "shop/product/list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "search_params": search_params,
        },
    )


def product_detail(request, slug):
    """
    View для отображения одного товара.
    slug приходит из URL (например: /product/gamer-pro-rtx-4060/).
    """
    # get_object_or_404 ищет товар по slug. Если не находит — показывает страницу 404
    product = get_object_or_404(Product, slug=slug, available=True)

    return render(request, "shop/product/detail.html", {"product": product})


def products_by_category(request, category_slug):
    """
    View для отображения товаров одной категории.
    category_slug приходит из URL (например: /category/igrovye-sborki/).
    """
    # Находим категорию по slug (или 404, если нет)
    category = get_object_or_404(Category, slug=category_slug)

    # Фильтруем товары: только этой категории + доступные
    products = Product.objects.filter(category=category, available=True)

    return render(
        request, "shop/category.html", {"category": category, "products": products}
    )


def cart_detail(request):
    """Показать содержимое корзины."""
    cart = Cart(request)
    return render(request, "shop/cart/detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    """Добавить товар в корзину."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if cart.has_product(product):
        # Товар уже в корзине — не добавляем повторно
        messages.warning(request, f'Сборка "{product.name}" уже добавлена в корзину!')
    else:
        cart.add(product=product, quantity=1, override_quantity=False)
        messages.success(request, f'Сборка "{product.name}" добавлена в корзину!')
    return redirect("shop:cart_detail")


@require_POST
def cart_add_ajax(request, product_id):
    """
    AJAX-добавление товара в корзину.
    Возвращает JSON вместо редиректа,
    чтобы JS на странице мог обновить счётчик и показать уведомление.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    if cart.has_product(product):
        # Товар уже в корзине — не добавляем повторно
        messages.warning(request, f'Сборка "{product.name}" уже добавлена в корзину!')
        return JsonResponse(
            {
                "success": False,
                "already_in_cart": True,
                "cart_total": len(cart),
                "product_name": product.name,
            }
        )
    
    cart.add(product=product, quantity=1, override_quantity=False)

    # Сохраняем сообщение — появится при следующем переходе на другую страницу
    messages.success(request, f'Товар "{product.name}" добавлен в корзину!')

    # Возвращаем JSON с результатом
    return JsonResponse(
        {
            "success": True,
            "cart_total": len(cart),  # общее количество товаров в корзине
            "product_name": product.name,  # имя товара для уведомления
        }
    )


@require_POST
def cart_remove(request, product_id):
    """Удалить товар из корзины."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    # <-- Добавить уведомление:
    messages.success(request, f'Товар "{product.name}" удалён из корзины!')
    return redirect("shop:cart_detail")


def order_create(request):
    """Оформление заказа."""
    cart = Cart(request)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Сохраняем заказ
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()

            # Создаём позиции заказа из корзины
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )

            # Очищаем корзину
            cart.clear()

            # <-- Добавить уведомление:
            messages.success(request, f"Заказ №{order.id} успешно оформлен!")

            # Перенаправляем на страницу подтверждения
            return redirect("shop:order_created")
    else:
        form = OrderForm()

    return render(request, "shop/order/create.html", {"cart": cart, "form": form})


def order_created(request):
    """Страница подтверждения заказа."""
    return render(request, "shop/order/created.html")


@login_required
def order_detail(request, order_id):
    """
    Детальная страница заказа.
    Показывает товары, количество, цены и общую сумму.
    Доступна только автору заказа.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, "shop/order/order_detail.html", {"order": order})


def register(request):
    """Регистрация нового пользователя."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Создаём пользователя
            user = form.save()
            # Автоматически входим пользователя
            login(request, user)
            # Перенаправляем на главную
            return redirect("shop:product_list")
    else:
        form = UserRegisterForm()

    return render(request, "shop/registration/register.html", {"form": form})


@require_POST
@login_required
def order_pay(request, order_id):
    """
    Имитация оплаты заказа пользователем.
    Меняет статус заказа с 'Новый' на 'Оплачен'.
    Доступно только для заказов текущего пользователя.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Проверяем, что заказ ещё не оплачен и не отменён
    if order.status == Order.STATUS_NEW:
        order.status = Order.STATUS_PAID
        order.save()
        messages.success(request, f"Заказ №{order.id} успешно оплачен!")
    else:
        messages.warning(
            request,
            f"Заказ №{order.id} нельзя оплатить — текущий статус: {order.get_status_display()}",
        )

    return redirect("shop:user_orders")


@login_required
def user_orders(request):
    """
    Страница 'Мои заказы' — показывает только заказы текущего пользователя.
    Доступна только авторизованным пользователям.
    """
    # Получаем все заказы текущего пользователя
    orders = Order.objects.filter(user=request.user)

    return render(request, "shop/orders/my_orders.html", {"orders": orders})


def about(request):
    """
    Страница 'О нас' — информация о компании, контакты, поддержка.
    Доступна всем пользователям без авторизации.
    """
    return render(request, "shop/about.html")

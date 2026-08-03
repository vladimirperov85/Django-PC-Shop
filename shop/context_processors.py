from .models import Category
from .cart import Cart  # ← Импортируем класс Cart


def categories(request):
    """
    Контекстный процессор.
    Автоматически добавляет список всех категорий в контекст любого шаблона.
    """
    return {
        "categories": Category.objects.all()
    }


def cart(request):
    """
    Контекстный процессор для корзины.
    Автоматически добавляет объект корзины в контекст любого шаблона.
    """
    return {
        "cart": Cart(request)
    }
# Django/Django-bboard/shop/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views  

# Имя приложения 
app_name = "shop"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("category/<slug:category_slug>/",views.products_by_category,name="products_by_category",),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/add-ajax/<int:product_id>/", views.cart_add_ajax, name="cart_add_ajax"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("order/create/", views.order_create, name="order_create"),
    path("order/created/", views.order_created, name="order_created"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("register/", views.register, name="register"),
    path("login/",auth_views.LoginView.as_view(template_name="shop/registration/login.html"),name="login",),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("my-orders/", views.user_orders, name="user_orders"),
    path("order/<int:order_id>/pay/", views.order_pay, name="order_pay"),
    path("about/", views.about, name="about"),
]

from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.index, name="index"),
    path("shop/", views.shop, name="shop"),
    path("cart/", views.cart, name="cart"),
    path('api/products/<int:pk>/', views.product_detail, name='get-product-detail'),
]
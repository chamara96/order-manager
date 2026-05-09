from django.urls import path

from . import views

app_name = "carts"
urlpatterns = [
    path("", views.cart_view, name="cart_view"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout_view, name="checkout"),
]

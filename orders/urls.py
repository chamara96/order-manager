from django.urls import path

from . import views

app_name = "orders"
urlpatterns = [
    path("my-orders/", views.find_my_orders_view, name="find_my_orders_view"),
    path(
        "my-orders/<str:order_number>",
        views.find_my_orders_view,
        name="find_my_orders_by_order_number_view",
    ),
    path(
        "order-placed/<str:order_number>", views.order_placed, name="order_placed_view"
    ),
]

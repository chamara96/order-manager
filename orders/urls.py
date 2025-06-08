from django.urls import path

from . import views

app_name = "orders"
urlpatterns = [
    path("my-orders/<str:order_number>", views.order_details, name="order_details"),
]
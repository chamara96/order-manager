from django.urls import path

from . import views

app_name = "products"
urlpatterns = [
    path("", views.index, name="index"),
    path("shop/", views.shop, name="shop"),
    path("products/<str:slug>/", views.product_detail, name="product-details"),
]

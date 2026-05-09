from django.http import Http404
from django.shortcuts import render

from .models import Order


def find_my_orders_view(request, order_number=None):
    order, error = None, None
    if request.method == "POST":
        order_number = request.POST.get("ordernumber")
    if request.method == "GET" and order_number:
        order_number = order_number.strip()
    if order_number:
        order = Order.objects.filter(order_number=order_number).first()
        if not order:
            error = "Invalid order number"
    return render(request, "pages/find-my-order.html", {"order": order, "error": error})


def order_placed(request, order_number):
    is_existing_order = Order.objects.filter(order_number=order_number).exists()
    if not is_existing_order:
        raise Http404("Order not found")
    return render(request, "pages/order-placed.html", {"order_number": order_number})

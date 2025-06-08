from django.shortcuts import render
from .models import Order


def order_details(request, order_number):

    order = Order.objects.filter(order_number=order_number).first()
    if not order:
        return render(request, "order_details.html", {"error": "Order not found."})

    context = {
        "order": order,
    }
    return render(request, "order_details.html", context)

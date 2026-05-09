from django.shortcuts import redirect, render

from orders.models import Order, OrderItem, State, Status
from products.models import Product

from .cart_service import CartService


def get_address_as_text(payload):
    streetaddress = payload.get("streetaddress")
    apt = payload.get("apt")
    city = payload.get("city")
    state = payload.get("state")
    zipcode = payload.get("zip")
    country = payload.get("country")
    address_parts = [streetaddress, apt, city, state, zipcode, country]
    return "\n".join(part for part in address_parts if part)


def get_payment_method(payload):
    method = payload.get("payment_method")
    if method == "bank_transfer":
        return "bank_transfer"
    return "cod"


def add_to_cart(request, product_id):
    CartService(request).add(product_id)
    return redirect("carts:cart_view")


def cart_view(request):
    if request.method == "POST":
        cart_service = CartService(request)

        remove_product_id = request.POST.get("remove")
        if remove_product_id:
            cart_service.remove(remove_product_id)
            return redirect("carts:cart_view")

        action = request.POST.get("action")
        if action == "clear":
            cart_service.clear()
        elif action == "update":
            payload = request.POST
            for key, value in payload.items():
                if key.startswith("quantities["):
                    product_id = key.split("[")[1].split("]")[0]
                    qty = int(value)
                    if qty > 0:
                        cart_service.update(product_id, qty)
                if key.startswith("notes["):
                    product_id = key.split("[")[1].split("]")[0]
                    note = value.strip()
                    cart_service.update_note(product_id, note)
        return redirect("carts:cart_view")
    return render(request, "pages/shopping-cart.html", {})


def checkout_view(request):
    if request.method == "POST":
        payload = request.POST
        print("Checkout Payload:\n", payload)  # Debugging line
        order = Order.objects.create(
            customer_name=payload.get("firstname") + " " + payload.get("lastname"),
            customer_phone=payload.get("phone"),
            customer_email=payload.get("email"),
            delivery_address=get_address_as_text(payload),
            payment_method=get_payment_method(payload),
        )
        if request.user.is_authenticated:
            cart = CartService(request).get_user_cart()
            for item in cart.items.select_related("product"):
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    note=item.note,
                    price=item.product.net_price * item.quantity,
                )
        else:
            cart = CartService(request).get_session_cart()
            products = Product.objects.filter(id__in=cart.keys())
            for product in products:
                qty = cart[str(product.id)].get("quantity", 0)
                note = cart[str(product.id)].get("note", "")
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    note=note,
                    price=product.net_price * qty,
                )
        CartService(request).clear()
        return redirect("orders:order_placed_view", order_number=order.order_number)
    return render(request, "pages/checkout.html", {})

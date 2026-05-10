from djmoney.money import Money

from carts.cart_service import CartService
from products.models import Product


def cart_context(request):
    service = CartService(request)
    items = []

    if request.user.is_authenticated:
        cart = service.get_user_cart()
        for item in cart.items.select_related("product"):
            items.append(
                {
                    "product": item.product,
                    "quantity": item.quantity,
                    "note": item.note,
                    "total": (
                        item.product.net_price * item.quantity
                        if item.product.stock > 0
                        else Money(0, "LKR")
                    ),
                }
            )
    else:
        session_cart = service.get_session_cart()
        products = Product.objects.filter(id__in=session_cart.keys())

        for product in products:
            qty = session_cart[str(product.id)].get("quantity", 0)
            note = session_cart[str(product.id)].get("note", "")
            items.append(
                {
                    "product": product,
                    "quantity": qty,
                    "note": note,
                    "total": (
                        product.net_price * qty
                        if product.stock > 0
                        else Money(0, "LKR")
                    ),
                }
            )
    cart_total = sum(item["total"] for item in items) or Money(0, "LKR")
    return {"cart_items": items, "cart_total": cart_total}

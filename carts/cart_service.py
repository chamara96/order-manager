from .models import Cart, CartItem


class CartService:

    def __init__(self, request):
        self.request = request
        self.session = request.session

    # -------------------------
    # SESSION CART
    # -------------------------
    def get_session_cart(self):
        return self.session.get("cart", {})

    def save_session_cart(self, cart):
        self.session["cart"] = cart
        self.session.modified = True

    # -------------------------
    # DB CART
    # -------------------------
    def get_user_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart

    # -------------------------
    # ADD ITEM
    # -------------------------
    def add(self, product_id, quantity=1):
        if self.request.user.is_authenticated:
            cart = self.get_user_cart()
            item, created = CartItem.objects.get_or_create(
                cart=cart, product_id=product_id
            )
            if not created:
                item.quantity += quantity
            item.save()
        else:
            cart = self.get_session_cart()
            product_id = str(product_id)

            if product_id in cart:
                cart[product_id]["quantity"] += quantity
            else:
                cart[product_id] = {"quantity": quantity}

            self.save_session_cart(cart)

    # -------------------------
    # REMOVE
    # -------------------------
    def remove(self, product_id):
        if self.request.user.is_authenticated:
            cart = self.get_user_cart()
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        else:
            cart = self.get_session_cart()
            product_id = str(product_id)
            if product_id in cart:
                del cart[product_id]
            self.save_session_cart(cart)

    # -------------------------
    # CLEAR
    # -------------------------
    def clear(self):
        if self.request.user.is_authenticated:
            cart = self.get_user_cart()
            cart.items.all().delete()
        else:
            self.save_session_cart({})

    # -------------------------
    # UPDATE
    # -------------------------
    def update(self, product_id, quantity: int):
        if self.request.user.is_authenticated:
            cart = self.get_user_cart()
            item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if item:
                item.quantity = quantity
                item.save()
        else:
            cart = self.get_session_cart()
            product_id = str(product_id)
            if product_id in cart:
                cart[product_id]["quantity"] = quantity
            self.save_session_cart(cart)

    def update_note(self, product_id, note: str):
        if self.request.user.is_authenticated:
            cart = self.get_user_cart()
            item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if item:
                item.note = note
                item.save()
        else:
            cart = self.get_session_cart()
            product_id = str(product_id)
            if product_id in cart:
                cart[product_id]["note"] = note
            self.save_session_cart(cart)

    # -------------------------
    # MERGE SESSION → DB
    # -------------------------
    def merge_session_to_db(self):
        if not self.request.user.is_authenticated:
            return

        session_cart = self.get_session_cart()
        if not session_cart:
            return

        cart = self.get_user_cart()

        for product_id, item in session_cart.items():
            obj, created = CartItem.objects.get_or_create(
                cart=cart, product_id=product_id
            )
            if not created:
                obj.quantity += item["quantity"]
                obj.note = item.get("note", "")
            else:
                obj.quantity = item["quantity"]
            obj.save()

        # clear session cart
        self.save_session_cart({})

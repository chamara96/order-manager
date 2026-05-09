from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from .cart_service import CartService


@receiver(user_logged_in)
def merge_cart(sender, request, user, **kwargs):
    cart_service = CartService(request)
    cart_service.merge_session_to_db()

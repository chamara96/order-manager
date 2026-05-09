from django.db import models

from products.models import Product

# from django.conf import settings


class Cart(models.Model):
    user = models.OneToOneField("base.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart ({self.user})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True, null=True, max_length=300)

    class Meta:
        unique_together = ("cart", "product")

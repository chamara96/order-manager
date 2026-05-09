import uuid

from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from base.models import BaseModel


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"
    CANCELLED = "cancelled", "Cancelled"


class Order(BaseModel):
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True, null=True)

    order_number = models.CharField(max_length=50, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_notes = models.TextField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)

    products = models.ManyToManyField(
        "products.Product",
        through="OrderItem",
        related_name="orders",
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("bank_transfer", "Bank Transfer"),
            ("cod", "Cash on Delivery"),
        ],
    )

    def __str__(self):
        return f"Order {self.order_number[:8]} - {self.customer_name}"

    @property
    def latest_status(self):
        status = self.statuses.order_by("-updated_at").first()
        return status.status.name if status else None

    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4()).replace("-", "").upper()
        super().save(*args, **kwargs)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True, null=True)
    price = MoneyField(max_digits=8, decimal_places=2, default_currency="LKR")

    def __str__(self):
        return f"{self.order}: {self.product.name} - {self.quantity} pcs"


class OrderStatus(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="statuses")
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    note = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        if self.pk:
            kwargs["update_fields"] = ["note"]
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order.order_number} - {self.status.name} - {self.updated_at}"

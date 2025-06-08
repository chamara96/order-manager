from django.db import models
from base.models import BaseModel
import uuid


class Order(BaseModel):
    customer_name = models.CharField(max_length=255)
    customer_address = models.TextField(blank=True, null=True)
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
            ("cod", "Cash on Delivery"),
            ("bank_transfer", "Bank Transfer"),
        ],
    )
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Order {self.order_number[:8]} - {self.customer_name}"
    
    def latest_status(self):
        status = self.statuses.order_by('-updated_at').first()
        return status.status.title() if status else 'N/A'
    
    def total_price(self):
        return sum(item.price for item in self.items.all())
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if not self.order_number:
            self.order_number = str(uuid.uuid4()).replace("-", "").upper()
        super().save(*args, **kwargs)
        
        # Auto-create initial status only for new orders
        if is_new:
            OrderStatus.objects.create(order=self, status='pending')


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} pcs"


class OrderStatus(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="statuses")
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("processing", "Processing"),
            ("shipped", "Shipped"),
            ("delivered", "Delivered"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.order.order_number} - {self.status} - {self.updated_at}"

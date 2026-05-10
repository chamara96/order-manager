import uuid
from decimal import Decimal

from django.db import models

# from base.templatetags.custom import currency
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from base.models import BaseModel


class Category(BaseModel):
    """
    Category model for product categorization.
    """

    name = models.CharField(max_length=128)
    slug = models.SlugField(default="")
    image = models.ImageField(upload_to="uploads/")
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, db_index=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["order"]


class ProductType(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(default="")
    image = models.ImageField(upload_to="product_types/", blank=True, null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Product(BaseModel):
    """
    Product model for storing product information.
    """

    name = models.CharField(max_length=128)
    slug = models.SlugField(default="")
    description = models.TextField(blank=True, null=True)
    price = MoneyField(max_digits=8, decimal_places=2, default_currency="LKR")
    sku = models.CharField(max_length=16, unique=True)
    stock = models.PositiveSmallIntegerField(default=None, blank=True, null=True)
    # image = models.ImageField(upload_to="uploads/")
    sizes = models.ManyToManyField(Size, related_name="products", blank=True)
    categories = models.ManyToManyField(
        Category,
        related_name="products",
        blank=True,
    )
    types = models.ManyToManyField(ProductType, related_name="products", blank=True)
    processing_time = models.PositiveSmallIntegerField(
        default=None, blank=True, null=True, help_text="Processing time in days"
    )
    trending = models.BooleanField(
        default=False, help_text="Mark product as trending, listed on homepage"
    )
    new = models.BooleanField(default=False, help_text="Mark product as new arrival")
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0, null=True, blank=True
    )
    discount_price = MoneyField(
        max_digits=8, decimal_places=2, null=True, blank=True, default_currency="LKR"
    )
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, db_index=True
    )

    def __str__(self):
        return self.name

    @property
    def formatted_discount_percentage(self):
        if self.discount_percentage and self.discount_percentage > 0:
            return format(self.discount_percentage.normalize(), "f")
        return None

    @property
    def has_discount(self):
        return (self.discount_percentage and self.discount_percentage > 0) or (
            self.discount_price and self.discount_price.amount > 0
        )

    @property
    def net_price(self):
        if (
            self.discount_percentage
            and self.discount_percentage > 0
            and self.discount_price == Money(0, "LKR")
        ):
            return self.price - (self.price * (self.discount_percentage / 100))
        if self.discount_price and self.discount_price.amount > 0:
            return self.discount_price
        return self.price

    @property
    def main_image(self):
        return self.images.first() if self.images.exists() else None

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self._generate_sku()
        super().save(*args, **kwargs)

    def _generate_sku(self):
        return f"WK{uuid.uuid4().hex[:6].upper()}"

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["order"]


class ProductImage(BaseModel):
    """
    Model for storing additional images for products.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(upload_to="uploads/")

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["product__order"]

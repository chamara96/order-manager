from django.db import models
from base.models import BaseModel
import uuid
from base.templatetags.custom import currency


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


class Tag(BaseModel):
    """
    Tag model for product tagging.
    """

    name = models.CharField(max_length=128)
    slug = models.SlugField(default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]


class ProductType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(BaseModel):
    """
    Product model for storing product information.
    """

    name = models.CharField(max_length=128)
    slug = models.SlugField(default="")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=64, unique=True)
    stock = models.PositiveIntegerField(default=0)
    # image = models.ImageField(upload_to="uploads/")
    categories = models.ManyToManyField(
        Category,
        related_name="products",
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="products",
        blank=True,
    )
    types = models.ManyToManyField(ProductType, related_name="products")
    is_popular = models.BooleanField(default=False)
    is_deal = models.BooleanField(default=False)
    discount_precent = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, db_index=True
    )

    def __str__(self):
        return self.name
    
    def calc_discount_price(self):
        if self.discount_precent > 0 and self.discount_price == 0:
            return self.price - (self.price * (self.discount_precent / 100))
        if self.discount_precent > 0 and self.discount_price > 0:
            return self.discount_price
        if self.discount_price > 0:
            return self.discount_price
        return self.price
    
    def calc_discount_price_formatted(self):
        return currency(self.calc_discount_price())
    
    def price_formatted(self):
        return currency(self.price)
    
    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = self._generate_sku()
        super().save(*args, **kwargs)

    def _generate_sku(self):
        return f'WK{uuid.uuid4().hex[:6].upper()}'
    

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

from django.db import models


class BaseModel(models.Model):
    """
    Base model with common fields for all models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class HomeSlider(BaseModel):
    title = models.CharField(max_length=128)
    category = models.CharField(max_length=16)
    image = models.ImageField(upload_to="uploads/")
    price_from = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, db_index=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Home Slider"
        verbose_name_plural = "Home Sliders"
        ordering = ["order"]

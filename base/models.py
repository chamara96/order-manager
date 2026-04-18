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
    header = models.CharField(max_length=20)
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    image = models.ImageField(upload_to="homeslider/")
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False, db_index=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Home Slider"
        verbose_name_plural = "Home Sliders"
        ordering = ["order"]


class SectionType(models.TextChoices):
    NEW_COLLECTION = "new_collection", "New Collection"
    SERVICES = "services", "Services"
    WHY_WITH_US = "why_with_us", "Why With Us"


class Section(BaseModel):
    type = models.CharField(max_length=20, choices=SectionType.choices)
    title = models.CharField(max_length=128)
    subtitle = models.CharField(max_length=255)
    icon_type_is_path = models.BooleanField(
        default=False,
        help_text="Indicates whether the icon is a path to an image file or a CSS class name for an icon font.",
    )
    icon = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title}"

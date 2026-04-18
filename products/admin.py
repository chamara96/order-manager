from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from base.templatetags.custom import currency

from .models import Category, Product, ProductImage, ProductType, Size


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("get_image", "name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    fieldsets = ((None, {"fields": ("name", "slug", "image", "is_active")}),)
    list_per_page = 20
    list_display_links = ("name",)

    def get_image(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" height="70" style="display: block;margin: auto;" />'
            )
        return "-"

    get_image.short_description = "Image"


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "image")
    ordering = ("name",)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False


class SizeAdmin(admin.ModelAdmin):
    pass


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    max_num = 5
    min_num = 1


class ProductAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "get_image",
        "slug",
        "price",
        "sku",
        "stock",
        "trending",
        "processing_time",
        "discount_percentage",
        "get_net_price",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "sku")
    list_filter = ("trending", "types")
    list_editable = (
        "price",
        "stock",
        "trending",
    )
    # fieldsets = (
    #     ("Details", {"fields": ("name", "slug", "description")}),
    #     ("Pricing and Stock", {"fields": ("price", "stock")}),
    #     (
    #         "Discounts and Promotions",
    #         {"fields": ("trending", "discount_price")},
    #     ),
    #     ("Categories and Tags", {"fields": ("categories", "tags")}),
    #     ("Product Types", {"fields": ("types",)}),
    # )
    inlines = [ProductImageInline]
    # save_as = True
    # save_on_top = True
    list_per_page = 20
    # list_select_related = True
    list_display_links = ("name",)

    def get_image(self, obj):
        if obj.images.exists():
            img = obj.images.first()
            return format_html(
                f'<img src="{img.image.url}" height="70" style="display: block;margin: auto;" />'
            )
        return "-"

    get_image.short_description = "Image"

    def get_net_price(self, obj):
        if obj.discount_percentage > 0 or obj.discount_price.amount > 0:
            return obj.net_price
        return "-"

    get_net_price.short_description = "Discount Price"


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Size, SizeAdmin)

from django.contrib import admin
from .models import Category, Tag, ProductType, Product, ProductImage
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from base.templatetags.custom import currency

class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("get_image","name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    fieldsets = (
        (None, {"fields": ("name", "slug", "image", "is_active")}),
    )
    list_per_page = 20
    list_display_links = ("name",)
    
    def get_image(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" height="70" style="display: block;margin: auto;" />')
        return "-"
    get_image.short_description = "Image"


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)
    fieldsets = ((None, {"fields": ("name", "slug")}),)
    save_as = True
    save_on_top = True
    list_per_page = 20
    list_max_show_all = 100
    list_select_related = True
    list_display_links = ("name",)


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False


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
        "is_popular",
        "is_deal",
        "discount_precent",
        "calculated_discount_price_new",
    )
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "sku")
    list_filter = ("is_popular", "is_deal", "types")
    list_editable = (
        "price",
        "stock",
        "is_popular",
        "is_deal"
    )
    fieldsets = (
        ("Details", {"fields": ("name", "slug", "description")}),
        ("Pricing and Stock", {"fields": ("price", "stock")}),
        (
            "Discounts and Promotions",
            {"fields": ("is_popular", "is_deal", "discount_precent", "discount_price")},
        ),
        ("Categories and Tags", {"fields": ("categories", "tags")}),
        ("Product Types", {"fields": ("types",)}),
    )
    inlines = [ProductImageInline]
    # save_as = True
    # save_on_top = True
    list_per_page = 20
    # list_select_related = True
    list_display_links = ("name",)
    
    def get_image(self, obj):
        if obj.images.exists():
            img = obj.images.first()
            return format_html(f'<img src="{img.image.url}" height="70" style="display: block;margin: auto;" />')
        return "-"
    get_image.short_description = "Image"

    def calculated_discount_price_new(self, obj):
        if obj.discount_precent:
            return currency(obj.calc_discount_price())
        return "-"
    calculated_discount_price_new.short_description = "Discount Price"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(Product, ProductAdmin)

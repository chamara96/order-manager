from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

# from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import HomeSlider, Section, User

# admin.site.unregister(User)
admin.site.unregister(Group)
# admin.site.unregister(Site)

admin.site.site_title = "Winks - Admin Panel"
admin.site.site_header = "Winks - Admin Panel"
admin.site.index_title = "Welcome to Winks Admin Panel"


class HomeSliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("get_image", "header", "title", "subtitle", "path", "is_active")
    # fieldsets = ((None, {"fields": ("title", "category", "price_from", "image", "is_active")}),)
    list_per_page = 20
    list_display_links = ("title",)

    def get_image(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" height="70" style="display: block;margin: auto;" />'
            )
        return "-"

    get_image.short_description = "Image"


class SectionAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "title",
        "subtitle",
        "icon_type_is_path",
        "icon",
        "is_active",
    )
    list_display_links = ("title",)


admin.site.register(HomeSlider, HomeSliderAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(User)

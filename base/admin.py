from django.contrib import admin
from .models import HomeSlider
from adminsortable2.admin import SortableAdminMixin
from django.utils.html import format_html

# from django.contrib.auth.models import User
# from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

# admin.site.unregister(User)
admin.site.unregister(Group)
# admin.site.unregister(Site)

admin.site.site_title = 'Winks - Admin Panel'
admin.site.site_header = 'Winks - Admin Panel'
admin.site.index_title = 'Welcome to Winks Admin Panel'


class HomeSliderAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("get_image", "title", "category", "price_from", "is_active")
    fieldsets = ((None, {"fields": ("title", "category", "price_from", "image", "is_active")}),)
    list_per_page = 20
    list_display_links = ("title",)

    def get_image(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" height="70" style="display: block;margin: auto;" />'
            )
        return "-"

    get_image.short_description = "Image"


admin.site.register(HomeSlider, HomeSliderAdmin)

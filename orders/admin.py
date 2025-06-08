from django.contrib import admin
from .models import Order, OrderItem, OrderStatus
from django.urls import path
from django.utils.html import format_html
from django.contrib import messages
from django.shortcuts import redirect


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # readonly_fields = ['price']
    autocomplete_fields = ['product']


class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    extra = 0
    readonly_fields = ['updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'customer_name',
        'order_date',
        'is_paid',
        'latest_status',
    )
    list_filter = (
        'statuses__status',
    )
    search_fields = (
        'order_number',
        'customer_name',
        'customer_email',
        'customer_phone',
    )
    date_hierarchy = 'order_date'
    inlines = [OrderItemInline]
    readonly_fields = ['order_number', 'order_date',"status_actions","status_history"]

    def latest_status(self, obj):
        status = obj.statuses.order_by('-updated_at').first()
        return status.status.title() if status else 'N/A'
    latest_status.short_description = 'Status'
    
    def status_actions(self, obj):
        if not obj.pk:
            return "(save order to update status)"
        actions = ""
        for status in ['processing', 'shipped', 'delivered', 'cancelled']:
            actions += f'<a class="button" style="margin-right:5px" href="{status}/">{status.title()}</a>'
        return format_html(actions)
    status_actions.short_description = "Change Status"
    status_actions.allow_tags = True
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:object_id>/change/<str:new_status>/', self.admin_site.admin_view(self.set_status), name='admin_set_status'),
        ]
        return custom_urls + urls
    
    def set_status(self, request, object_id, new_status):
        order = Order.objects.get(pk=object_id)
        if new_status not in dict(OrderStatus._meta.get_field('status').choices):
            messages.error(request, f"Invalid status: {new_status}")
        else:
            OrderStatus.objects.create(order=order, status=new_status)
            messages.success(request, f"Order status set to {new_status.title()}")
        return redirect(f'/admin/orders/order/')
    
    def status_history(self, obj):
        return format_html('<br>'.join(
            f"{s.updated_at.strftime('%Y-%m-%d %H:%M:%S')} — {s.status.title()}"
            for s in obj.statuses.all()
        ))
    status_history.short_description = "Status History"


from django.contrib import admin, messages
from django.forms.models import BaseInlineFormSet
from django.shortcuts import redirect
from django.urls import path
from django.utils.html import format_html

from .models import Order, OrderItem, OrderStatus, Status


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["product", "quantity", "note", "price"]
    fields = ["product", "quantity", "note", "price"]

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class OrderStatusInlineFormSet(BaseInlineFormSet):

    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)

        if form.instance and form.instance.pk:
            for field in form.fields.values():
                if field.label == "Status":
                    field.disabled = True
                    field.widget.can_add_related = False
                    field.widget.can_change_related = False
                    field.widget.can_view_related = False
                    field.widget.can_delete_related = False

        return form


class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    formset = OrderStatusInlineFormSet
    extra = 1
    readonly_fields = ["updated_at"]
    fields = ["status", "note", "updated_at"]

    # def get_readonly_fields(self, request, obj = None):
    #     if obj:
    #         return self.readonly_fields + ["status"]
    #     return self.readonly_fields

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "note":
            formfield.widget.attrs["rows"] = 2
        return formfield

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == "status":  # your FK field name
            formfield.widget.can_add_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_view_related = False

        return formfield


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "customer_name",
        "order_date",
        "latest_status",
    )
    list_filter = ("statuses__status",)
    search_fields = (
        "order_number",
        "customer_name",
        "customer_email",
        "customer_phone",
    )
    date_hierarchy = "order_date"
    inlines = [OrderItemInline, OrderStatusInline]
    readonly_fields = [
        "order_number",
        "customer_link",
        "order_date",
        "status_actions",
        "status_history",
    ]

    def status_actions(self, obj):
        if not obj.pk:
            return "(save order to update status)"
        is_finalized_order = OrderStatus.objects.filter(
            order=obj, status__name__in=["Completed", "Cancelled"]
        ).exists()
        if is_finalized_order:
            return "No actions available for completed or cancelled orders"
        actions = ""
        available_statuses = ["completed", "cancelled"]
        if obj.latest_status is None:
            available_statuses = ["accepted", "cancelled"]

        for status in available_statuses:
            actions += f'<a class="button" style="margin-right:5px" href="{status}/">{status.title()}</a>'
        return format_html(actions)

    status_actions.short_description = "Change Status"
    status_actions.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:object_id>/change/<str:new_status>/",
                self.admin_site.admin_view(self.set_status),
                name="admin_set_status",
            ),
        ]
        return custom_urls + urls

    def set_status(self, request, object_id, new_status: str):
        order = Order.objects.get(pk=object_id)
        new_status, _ = Status.objects.get_or_create(name=new_status.title())
        OrderStatus.objects.get_or_create(order=order, status=new_status)
        messages.success(request, f"Order status set to {new_status.name}")
        return redirect(f"/admin/orders/order/")

    def status_history(self, obj):
        return format_html(
            "<br>".join(
                f"{s.updated_at.strftime('%Y-%m-%d %H:%M:%S')} — {s.status.name}"
                for s in obj.statuses.all()
            )
        )

    status_history.short_description = "Status History"

    def customer_link(self, obj):
        if not obj.pk:
            return "(save order to view customer link)"
        return format_html(
            f"<a target='_blank' href='/my-orders/{obj.order_number}'>Click</a>"
        )

    customer_link.short_description = "Customer Link"


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass

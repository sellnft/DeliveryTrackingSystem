from django.contrib import admin

from .models import Order, Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("id", "origin_address", "delivery_address")
    search_fields = ("origin_address", "delivery_address")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "courier", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("description", "client__username", "courier__username")
    readonly_fields = ("created_at", "updated_at")

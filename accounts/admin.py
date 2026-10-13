from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "full_name", "role", "phone", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("username", "full_name", "phone")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Дополнительно", {"fields": ("full_name", "role", "phone")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Дополнительно", {"fields": ("full_name", "role", "phone")}),
    )

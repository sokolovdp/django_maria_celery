from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import RewardLog, ScheduledReward, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "coins", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email", "coins")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2", "coins"),
            },
        ),
    )


@admin.register(ScheduledReward)
class ScheduledRewardAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "execute_at", "is_executed")
    list_filter = ("is_executed", "execute_at")
    search_fields = ("user__username",)
    date_hierarchy = "execute_at"


@admin.register(RewardLog)
class RewardLogAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "given_at", "reason")
    list_filter = ("given_at",)
    search_fields = ("user__username", "reason")
    date_hierarchy = "given_at"
    readonly_fields = ("given_at",)

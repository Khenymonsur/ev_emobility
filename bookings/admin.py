from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "service_type", "pickup_location", "destination", "date", "time", "status", "created_at")
    list_filter = ("service_type", "status", "date", "created_at")
    search_fields = ("name", "email", "phone", "pickup_location", "destination")
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("status",)
    fieldsets = (
        ("Customer", {"fields": ("name", "phone", "email")}),
        ("Trip", {"fields": ("service_type", "pickup_location", "destination", "date", "time")}),
        ("Admin", {"fields": ("status", "admin_notes")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

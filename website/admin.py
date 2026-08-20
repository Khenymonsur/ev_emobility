from django.contrib import admin

from .models import ChargingStation, ContactMessage, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("name", "vehicle_type", "seats", "estimated_range_km", "is_active", "display_order")
    list_filter = ("vehicle_type", "is_active")
    search_fields = ("name", "vehicle_type")
    list_editable = ("is_active", "display_order")


@admin.register(ChargingStation)
class ChargingStationAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "charger_type", "available_chargers", "total_chargers", "is_active")
    list_filter = ("charger_type", "is_active")
    search_fields = ("name", "location", "charger_type")
    list_editable = ("available_chargers", "is_active")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "phone", "message")
    readonly_fields = ("created_at",)
    list_editable = ("is_read",)

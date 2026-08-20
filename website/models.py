from django.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=120)
    vehicle_type = models.CharField(max_length=80)
    seats = models.PositiveSmallIntegerField(default=5)
    estimated_range_km = models.PositiveIntegerField(help_text="Estimated driving range in kilometers.")
    image = models.FileField(upload_to="vehicles/", blank=True, help_text="Optional uploaded vehicle image.")
    image_url = models.URLField(blank=True, help_text="Optional external image URL if no upload is available.")
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class ChargingStation(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=180)
    charger_type = models.CharField(max_length=80)
    available_chargers = models.PositiveSmallIntegerField(default=1)
    total_chargers = models.PositiveSmallIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.location}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"

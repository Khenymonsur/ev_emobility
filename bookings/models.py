from django.db import models


class Booking(models.Model):
    class ServiceType(models.TextChoices):
        RIDE = "ride", "Ride"
        RENTAL = "rental", "Rental"
        SCHEDULED_RIDE = "scheduled_ride", "Scheduled Ride"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    service_type = models.CharField(max_length=32, choices=ServiceType.choices)
    pickup_location = models.CharField(max_length=180)
    destination = models.CharField(max_length=180)
    date = models.DateField()
    time = models.TimeField()
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()} on {self.date}"

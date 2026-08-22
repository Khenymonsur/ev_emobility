from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.urls import reverse

from bookings.forms import BookingForm
from website.forms import ContactForm
from website.models import ChargingStation, Vehicle


FALLBACK_VEHICLES = [
    {
        "name": "Tesla Model 3",
        "vehicle_type": "Premium sedan",
        "seats": 5,
        "estimated_range_km": 438,
    },
    {
        "name": "BYD Atto 3",
        "vehicle_type": "Compact SUV",
        "seats": 5,
        "estimated_range_km": 420,
    },
    {
        "name": "Hyundai Kona Electric",
        "vehicle_type": "Urban SUV",
        "seats": 5,
        "estimated_range_km": 484,
    },
    {
        "name": "Nissan Leaf",
        "vehicle_type": "City hatchback",
        "seats": 5,
        "estimated_range_km": 270,
    },
]

FALLBACK_CHARGERS = [
    {"name": "Victoria Island Hub", "location": "Victoria Island, Lagos", "charger_type": "DC Fast", "available_chargers": 6},
    {"name": "Ikeja Mobility Point", "location": "Ikeja, Lagos", "charger_type": "AC + DC", "available_chargers": 4},
    {"name": "Lekki Solar Station", "location": "Lekki Phase 1, Lagos", "charger_type": "DC Fast", "available_chargers": 8},
]


def notify_admin(subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.BOOKING_NOTIFICATION_EMAIL],
        fail_silently=True,
    )


def get_vehicles():
    return Vehicle.objects.filter(is_active=True).order_by("display_order", "name")


def get_charging_stations():
    return ChargingStation.objects.filter(is_active=True).order_by("name")


def get_charging_summary(charging_stations):
    charging_totals = charging_stations.aggregate(
        total_chargers=Sum("total_chargers"),
        available_chargers=Sum("available_chargers"),
    )
    charger_types = sorted({station.charger_type for station in charging_stations})

    if charging_stations.exists():
        return {
            "station_count": charging_stations.count(),
            "available_chargers": charging_totals["available_chargers"] or 0,
            "total_chargers": charging_totals["total_chargers"] or 0,
            "charger_types": " / ".join(charger_types),
        }

    fallback_types = sorted({station["charger_type"] for station in FALLBACK_CHARGERS})
    return {
        "station_count": len(FALLBACK_CHARGERS),
        "available_chargers": sum(station["available_chargers"] for station in FALLBACK_CHARGERS),
        "total_chargers": sum(station["available_chargers"] for station in FALLBACK_CHARGERS),
        "charger_types": " / ".join(fallback_types),
    }


def site_context(**extra):
    charging_stations = get_charging_stations()
    context = {
        "vehicles": get_vehicles(),
        "fallback_vehicles": FALLBACK_VEHICLES,
        "charging_stations": charging_stations,
        "charging_summary": get_charging_summary(charging_stations),
        "fallback_chargers": FALLBACK_CHARGERS,
    }
    context.update(extra)
    return context


def handle_booking_form(request, redirect_target):
    booking_form = BookingForm(request.POST, prefix="booking")
    if booking_form.is_valid():
        booking = booking_form.save()
        notify_admin(
            "New EV mobility booking request",
            (
                f"New booking request from {booking.name}\n\n"
                f"Service: {booking.get_service_type_display()}\n"
                f"Pickup: {booking.pickup_location}\n"
                f"Destination: {booking.destination}\n"
                f"Date: {booking.date}\n"
                f"Time: {booking.time}\n"
                f"Phone: {booking.phone}\n"
                f"Email: {booking.email}"
            ),
        )
        messages.success(request, "Your booking request has been received. Our team will contact you shortly.")
        return redirect(redirect_target), BookingForm(prefix="booking")

    messages.error(request, "Please correct the booking details and try again.")
    return None, booking_form


def handle_contact_form(request, redirect_target):
    contact_form = ContactForm(request.POST, prefix="contact")
    if contact_form.is_valid():
        contact = contact_form.save()
        notify_admin(
            "New website contact message",
            (
                f"New contact message from {contact.name}\n\n"
                f"Phone: {contact.phone}\n"
                f"Email: {contact.email}\n\n"
                f"{contact.message}"
            ),
        )
        messages.success(request, "Thanks for reaching out. We will reply as soon as possible.")
        return redirect(redirect_target), ContactForm(prefix="contact")

    messages.error(request, "Please correct the contact form and try again.")
    return None, contact_form


def home(request):
    booking_form = BookingForm(prefix="booking")
    contact_form = ContactForm(prefix="contact")

    if request.method == "POST":
        form_kind = request.POST.get("form_kind")

        if form_kind == "booking":
            response, booking_form = handle_booking_form(request, f"{reverse('core:home')}#booking")
            if response:
                return response

        if form_kind == "contact":
            response, contact_form = handle_contact_form(request, f"{reverse('core:home')}#contact")
            if response:
                return response

    return render(
        request,
        "core/home.html",
        site_context(booking_form=booking_form, contact_form=contact_form),
    )


def about(request):
    return render(request, "core/about.html", site_context())


def services(request):
    return render(request, "core/services.html", site_context())


def vehicles(request):
    return render(request, "core/vehicles.html", site_context())


def charge_station(request):
    return render(request, "core/charge_station.html", site_context())


def corporate(request):
    return render(request, "core/corporate.html", site_context())


def gallery(request):
    return render(request, "core/gallery.html", site_context())


def contact(request):
    contact_form = ContactForm(prefix="contact")
    if request.method == "POST":
        response, contact_form = handle_contact_form(request, reverse("core:contact"))
        if response:
            return response
    return render(request, "core/contact.html", site_context(contact_form=contact_form))


def booking(request):
    booking_form = BookingForm(prefix="booking")
    if request.method == "POST":
        response, booking_form = handle_booking_form(request, reverse("core:booking"))
        if response:
            return response
    return render(request, "core/booking.html", site_context(booking_form=booking_form))


def download_app(request):
    return render(request, "core/download_app.html")


def privacy_policy(request):
    return render(request, "core/privacy_policy.html")


def terms_conditions(request):
    return render(request, "core/terms_conditions.html")

from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from bookings.models import Booking
from website.models import ContactMessage


class HomePageTests(TestCase):
    def test_public_pages_render(self):
        pages = [
            ("core:about", "Silent streets"),
            ("core:services", "All your electric mobility needs"),
            ("core:vehicles", "Electric vehicles for rides"),
            ("core:charge_station", "Charging operations"),
            ("core:corporate", "Electric mobility for your business"),
            ("core:gallery", "Clean mobility"),
            ("core:contact", "We would love to hear from you"),
            ("core:booking", "Request an electric ride"),
        ]

        for route_name, expected_text in pages:
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected_text)

    def test_homepage_renders(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Move Smarter. Go Electric.")
        self.assertContains(response, "Request Booking")
        self.assertContains(response, reverse("core:privacy_policy"))
        self.assertContains(response, reverse("core:terms_conditions"))

    def test_legal_pages_render(self):
        privacy_response = self.client.get(reverse("core:privacy_policy"))
        terms_response = self.client.get(reverse("core:terms_conditions"))

        self.assertEqual(privacy_response.status_code, 200)
        self.assertContains(privacy_response, "Privacy Policy")
        self.assertEqual(terms_response.status_code, 200)
        self.assertContains(terms_response, "Terms &amp; Conditions")

    def test_booking_form_submission_creates_booking(self):
        trip_date = timezone.localdate() + timedelta(days=7)
        response = self.client.post(
            reverse("core:home"),
            {
                "form_kind": "booking",
                "booking-service_type": Booking.ServiceType.RIDE,
                "booking-pickup_location": "Ikoyi",
                "booking-destination": "Ikeja",
                "booking-date": trip_date.isoformat(),
                "booking-time": "09:30",
                "booking-name": "Ada Customer",
                "booking-phone": "+2348000000000",
                "booking-email": "ada@example.com",
            },
        )

        self.assertRedirects(response, f"{reverse('core:home')}#booking")
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_page_form_submission_creates_booking(self):
        trip_date = timezone.localdate() + timedelta(days=7)
        response = self.client.post(
            reverse("core:booking"),
            {
                "form_kind": "booking",
                "booking-service_type": Booking.ServiceType.SCHEDULED_RIDE,
                "booking-pickup_location": "Lekki",
                "booking-destination": "Airport",
                "booking-date": trip_date.isoformat(),
                "booking-time": "07:15",
                "booking-name": "Mina Customer",
                "booking-phone": "+2348000000002",
                "booking-email": "mina@example.com",
            },
        )

        self.assertRedirects(response, reverse("core:booking"))
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_form_rejects_past_date(self):
        trip_date = timezone.localdate() - timedelta(days=1)
        response = self.client.post(
            reverse("core:home"),
            {
                "form_kind": "booking",
                "booking-service_type": Booking.ServiceType.RIDE,
                "booking-pickup_location": "Ikoyi",
                "booking-destination": "Ikeja",
                "booking-date": trip_date.isoformat(),
                "booking-time": "09:30",
                "booking-name": "Ada Customer",
                "booking-phone": "+2348000000000",
                "booking-email": "ada@example.com",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please choose today or a future date.")
        self.assertEqual(Booking.objects.count(), 0)

    def test_contact_form_submission_creates_message(self):
        response = self.client.post(
            reverse("core:home"),
            {
                "form_kind": "contact",
                "contact-name": "Tunde Client",
                "contact-email": "tunde@example.com",
                "contact-phone": "+2348000000001",
                "contact-message": "We need corporate EV transport.",
            },
        )

        self.assertRedirects(response, f"{reverse('core:home')}#contact")
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_contact_page_form_submission_creates_message(self):
        response = self.client.post(
            reverse("core:contact"),
            {
                "form_kind": "contact",
                "contact-name": "Corporate Lead",
                "contact-email": "fleet@example.com",
                "contact-phone": "+2348000000003",
                "contact-message": "We need EV fleet support.",
            },
        )

        self.assertRedirects(response, reverse("core:contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)

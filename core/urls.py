from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("vehicles/", views.vehicles, name="vehicles"),
    path("charge-station/", views.charge_station, name="charge_station"),
    path("corporate/", views.corporate, name="corporate"),
    path("gallery/", views.gallery, name="gallery"),
    path("contact/", views.contact, name="contact"),
    path("booking/", views.booking, name="booking"),
    path("privacy/", views.privacy_policy, name="privacy_policy"),
    path("terms/", views.terms_conditions, name="terms_conditions"),
]

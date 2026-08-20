from django import forms
from django.utils import timezone

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            "service_type",
            "pickup_location",
            "destination",
            "date",
            "time",
            "name",
            "phone",
            "email",
        ]
        widgets = {
            "service_type": forms.Select(attrs={"class": "form-select"}),
            "pickup_location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Pickup location"}),
            "destination": forms.TextInput(attrs={"class": "form-control", "placeholder": "Destination"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
        }

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date < timezone.localdate():
            raise forms.ValidationError("Please choose today or a future date.")
        return date

# CloudRide EV Mobility Website

A clean Django first version for an African electric mobility company. The site presents EV rides, rentals, scheduled bookings, corporate transport, charging access, fleet services, gallery content, legal pages, and simple customer contact flows.

## Stack

- Django 6.1
- SQLite for development
- Bootstrap 5
- Plain CSS and JavaScript

## Apps

- `core`: public homepage and form handling
- `bookings`: booking model, form, and admin workflow
- `website`: vehicles, charging stations, and contact messages

## Local Setup

```bash
python manage.py migrate
python manage.py seed_demo_content
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Open `http://127.0.0.1:8000/`.

Admin is available at `http://127.0.0.1:8000/admin/`.

## Public Pages

- `/`
- `/about/`
- `/services/`
- `/vehicles/`
- `/charge-station/`
- `/corporate/`
- `/gallery/`
- `/contact/`
- `/booking/`
- `/privacy/`
- `/terms/`

## Admin Content

Django Admin can manage:

- Vehicles
- Booking requests
- Charging stations
- Contact messages

Booking statuses:

- Pending
- Confirmed
- Completed
- Cancelled

## Development Notes

Email notifications use the console backend during development. Production should configure a real mail backend, environment-based secrets, secure cookies, HTTPS settings, and a production database such as PostgreSQL or MySQL.

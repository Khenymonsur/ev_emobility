from django.core.management.base import BaseCommand

from website.models import ChargingStation, Vehicle


VEHICLES = [
    {
        "name": "Tesla Model 3",
        "vehicle_type": "Premium sedan",
        "seats": 5,
        "estimated_range_km": 438,
        "display_order": 1,
    },
    {
        "name": "BYD Atto 3",
        "vehicle_type": "Compact SUV",
        "seats": 5,
        "estimated_range_km": 420,
        "display_order": 2,
    },
    {
        "name": "Hyundai Kona Electric",
        "vehicle_type": "Urban SUV",
        "seats": 5,
        "estimated_range_km": 484,
        "display_order": 3,
    },
    {
        "name": "Nissan Leaf",
        "vehicle_type": "City hatchback",
        "seats": 5,
        "estimated_range_km": 270,
        "display_order": 4,
    },
]

CHARGING_STATIONS = [
    {
        "name": "Victoria Island Hub",
        "location": "Victoria Island, Lagos",
        "charger_type": "DC Fast",
        "available_chargers": 6,
        "total_chargers": 8,
    },
    {
        "name": "Ikeja Mobility Point",
        "location": "Ikeja, Lagos",
        "charger_type": "AC + DC",
        "available_chargers": 4,
        "total_chargers": 6,
    },
    {
        "name": "Lekki Solar Station",
        "location": "Lekki Phase 1, Lagos",
        "charger_type": "DC Fast",
        "available_chargers": 8,
        "total_chargers": 10,
    },
    {
        "name": "Airport Express Charge",
        "location": "Murtala Muhammed Airport Road, Lagos",
        "charger_type": "AC",
        "available_chargers": 3,
        "total_chargers": 4,
    },
]


class Command(BaseCommand):
    help = "Seed demo vehicles and charging stations for the EV mobility website."

    def handle(self, *args, **options):
        vehicle_count = 0
        station_count = 0

        for vehicle in VEHICLES:
            _, created = Vehicle.objects.update_or_create(
                name=vehicle["name"],
                defaults={**vehicle, "is_active": True},
            )
            vehicle_count += int(created)

        for station in CHARGING_STATIONS:
            _, created = ChargingStation.objects.update_or_create(
                name=station["name"],
                defaults={**station, "is_active": True},
            )
            station_count += int(created)

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo content ready. Created {vehicle_count} vehicles and {station_count} charging stations."
            )
        )

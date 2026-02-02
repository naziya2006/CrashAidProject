import os
import sys
import django
import json
import datetime
from django.utils import timezone

# Project root ko path me add karo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crashaid.settings")
django.setup()

from accidents.models import Accident

# Load cleaned JSON
with open("C:/Users/naziy/CrashAidProject/data/cleaned_accidents.json", "r") as f:
    data = json.load(f)

for entry in data:
    naive_dt = datetime.datetime.fromisoformat(entry["timestamp"])
    aware_dt = timezone.make_aware(naive_dt)
    Accident.objects.update_or_create(
        location=entry["location"],
        latitude=entry["latitude"],
        longitude=entry["longitude"],
        time=aware_dt,
        defaults={
            "severity": entry.get("severity", "Unknown"),
            "description": entry.get("description", "")
        }
    )

print("Accidents data loaded successfully!")



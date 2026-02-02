from django.db import models
from accounts.models import Hospital
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from django.utils import timezone


class Accident(models.Model):
    SEVERITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    location = models.CharField(max_length=200)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    nearest_hospital = models.ForeignKey(
        Hospital, null=True, blank=True, on_delete=models.SET_NULL
    )
    hospital = models.CharField(max_length=200, blank=True, null=True)

    handled = models.BooleanField(default=False)
    alert_sent = models.BooleanField(default=False)
    time = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        """
        Automatically calculate latitude/longitude and nearest hospital
        """

        # Auto geocode location if lat/lon not provided
        if self.latitude == 0.0 and self.longitude == 0.0 and self.location:
            geolocator = Nominatim(user_agent="crashaid_app")
            try:
                loc = geolocator.geocode(self.location)
                if loc:
                    self.latitude = loc.latitude
                    self.longitude = loc.longitude
            except:
                pass

        # Assign nearest hospital automatically (only first save)
        if not self.pk and self.latitude and self.longitude:
            hospitals = Hospital.objects.exclude(
                latitude__isnull=True,
                longitude__isnull=True
            )

            nearest = min(
                hospitals,
                key=lambda h: geodesic(
                    (self.latitude, self.longitude),
                    (h.latitude, h.longitude)
                ).km,
                default=None
            )

            if nearest:
                self.nearest_hospital = nearest
                self.hospital = nearest.name

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.location} - {self.severity}"

from django.db import models
from geopy.geocoders import Nominatim

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        # Auto geocode hospital address if lat/lon not provided
        if (self.latitude == 0.0 or self.longitude == 0.0) and self.address:
            geolocator = Nominatim(user_agent="crashaid_app")
            try:
                loc = geolocator.geocode(self.address)
                if loc:
                    self.latitude = loc.latitude
                    self.longitude = loc.longitude
            except:
                pass  # ignore geocode errors
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

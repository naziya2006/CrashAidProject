# hospitalapp/models.py
from django.db import models
from geopy.geocoders import Nominatim

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # city/address
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)  # ✅ add this
    longitude = models.FloatField(blank=True, null=True) # ✅ add this
    added_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if (self.latitude is None) or (self.longitude is None):
            geolocator = Nominatim(user_agent="crashaidproject")
            try:
                loc = geolocator.geocode(self.location)
                if loc:
                    self.latitude = loc.latitude
                    self.longitude = loc.longitude
            except:
                pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Ambulance(models.Model):
    name = models.CharField(max_length=100)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            # Ambulance ko hospital ke location se set karenge
            if self.hospital and self.hospital.latitude and self.hospital.longitude:
                self.latitude = self.hospital.latitude
                self.longitude = self.hospital.longitude
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

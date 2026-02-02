from django.db import models

# -----------------------
# Hospital Model
# -----------------------
class Hospital(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    contact = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# -----------------------
# Accident Model
# -----------------------
class Accident(models.Model):
    location = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    severity = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now_add=True)
    nearest_hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.location} - {self.severity}"

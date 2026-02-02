from django.contrib import admin
from .models import Accident

@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    list_display = (
        'location',
        'severity',
        'hospital',
        'latitude',
        'longitude',
        'handled',
        'alert_sent',
        'time'
    )

    # Ye fields user ke liye read-only hain, automatically calculate hote hain
    readonly_fields = (
        'latitude',
        'longitude',
        'nearest_hospital',
        'hospital',
        'time'
    )

    # Form me user sirf ye fill karega
    fields = (
        'location',
        'severity',
        'description',
        'latitude',
        'longitude',
        'nearest_hospital',
        'hospital',
        'handled',
        'alert_sent',
        'time'
    )

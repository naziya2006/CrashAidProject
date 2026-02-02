# hospitalapp/admin.py
from django.contrib import admin
from .models import Hospital

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'latitude', 'longitude')
    search_fields = ('name', 'location', 'address')

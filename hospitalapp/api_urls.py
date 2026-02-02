from django.urls import path
from .api_views import HospitalListAPI

urlpatterns = [
    path('hospital/', HospitalListAPI.as_view(), name='api_hospital'),
]

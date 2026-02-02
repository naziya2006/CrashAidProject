from django.urls import path
from .api_views import AccidentListAPI, LatestAccidentsAPI, HospitalListAPI

urlpatterns = [
    path('accident/', AccidentListAPI.as_view(), name='api_accident'),
    path('latest_accidents/', LatestAccidentsAPI.as_view(), name='api_latest_accidents'),
    path('hospitals/', HospitalListAPI.as_view(), name='api_hospitals'),
]

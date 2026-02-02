from rest_framework import generics
from .models import Accident
from .serializers import AccidentSerializer
from hospitalapp.models import Hospital
from hospitalapp.serializers import HospitalSerializer

class AccidentListAPI(generics.ListCreateAPIView):
    queryset = Accident.objects.all().order_by('-time')
    serializer_class = AccidentSerializer

class LatestAccidentsAPI(generics.ListAPIView):
    queryset = Accident.objects.all().order_by('-time')[:5]
    serializer_class = AccidentSerializer

class HospitalListAPI(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

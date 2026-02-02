from rest_framework import generics
from .models import Hospital
from .serializers import HospitalSerializer

class HospitalListAPI(generics.ListAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

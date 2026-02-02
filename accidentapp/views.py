from django.shortcuts import render, get_object_or_404, redirect
from .models import Accident
from .forms import AccidentForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from accounts.models import Hospital
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# ---------- Accident List ----------
def accident_list(request):
    accidents = Accident.objects.all().order_by('-time')
    return render(request, 'accidentapp/accident_list.html', {'accidents': accidents})

# ---------- Accident Detail ----------
def accident_detail(request, pk):
    accident = get_object_or_404(Accident, pk=pk)
    return render(request, 'accidentapp/accident_detail.html', {'accident': accident})

# ---------- Add Accident via Form ----------
def add_accident(request):
    if request.method == "POST":
        location = request.POST.get('location')
        severity = request.POST.get('severity')
        description = request.POST.get('description')
        hospital = request.POST.get('hospital')
        latitude = float(request.POST.get('latitude') or 0.0)
        longitude = float(request.POST.get('longitude') or 0.0)

        # Ensure coordinates are valid for India
        if not (6 <= latitude <= 38 and 68 <= longitude <= 97):
            latitude = 20.5937   # fallback: India center
            longitude = 78.9629

        accident = Accident.objects.create(
            location=location,
            severity=severity,
            description=description,
            hospital=hospital,
            latitude=latitude,
            longitude=longitude
        )
        return redirect('/accidentapp/')
    return render(request, 'accidentapp/add_accident.html')

# ---------- Map View ----------
def map_view(request):
    accidents = Accident.objects.filter(latitude__isnull=False, longitude__isnull=False)
    accident_list_data = []

    for acc in accidents:
        if 6 <= acc.latitude <= 38 and 68 <= acc.longitude <= 97:
            accident_list_data.append({
                'id': acc.id,
                'location': acc.location,
                'severity': acc.severity,
                'latitude': acc.latitude,
                'longitude': acc.longitude,
                'hospital': acc.hospital,
            })

    return render(request, 'accidentapp/map_view.html', {'accidents': json.dumps(accident_list_data)})

# ---------- IoT Accident API ----------
@csrf_exempt
def iot_accident(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            location = data.get("location", "Unknown Location")
            latitude = float(data.get("latitude", 0.0))
            longitude = float(data.get("longitude", 0.0))
            severity = data.get("severity", "Low")
            description = data.get("description", "")

            # Fix invalid coordinates
            if latitude < 6 or latitude > 38 or longitude < 68 or longitude > 97:
                geolocator = Nominatim(user_agent="crashaid_app")
                loc = geolocator.geocode(location)
                if loc:
                    latitude = loc.latitude
                    longitude = loc.longitude
                else:
                    latitude = 20.5937
                    longitude = 78.9629

            # Nearest hospital calculation
            hospitals = Hospital.objects.exclude(latitude__isnull=True, longitude__isnull=True)
            nearest = None
            min_distance = None
            for h in hospitals:
                dist = geodesic((latitude, longitude), (h.latitude, h.longitude)).km
                if min_distance is None or dist < min_distance:
                    min_distance = dist
                    nearest = h

            accident = Accident.objects.create(
                location=location,
                latitude=latitude,
                longitude=longitude,
                severity=severity,
                description=description,
                nearest_hospital=nearest,
                hospital=nearest.name if nearest else ""
            )

            return JsonResponse({"status": "success", "accident_id": accident.id})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Only POST allowed"})

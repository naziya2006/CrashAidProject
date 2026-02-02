from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from accounts.models import Hospital
from accidentapp.models import Accident
import json

# ---------------------------
# Hospital Dashboard Views
# ---------------------------

def dashboard(request, hospital_id):
    """
    Hospital Dashboard: Shows latest 10 accidents assigned to this hospital
    """
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    accidents = Accident.objects.filter(nearest_hospital=hospital).order_by('-time')[:10]
    return render(request, 'hospitalapp/dashboard.html', {
        'hospital': hospital,
        'accidents': accidents
    })


def latest_accident_alerts(request, hospital_id):
    """
    API: Return latest accident alerts for this hospital as JSON
    """
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    alerts = Accident.objects.filter(nearest_hospital=hospital, alert_sent=True).order_by('-time')[:10]
    data = []
    for acc in alerts:
        data.append({
            "id": acc.id,
            "location": acc.location,
            "severity": acc.severity,
            "latitude": acc.latitude,
            "longitude": acc.longitude,
            "time": acc.time.strftime("%Y-%m-%d %H:%M:%S"),
            "handled": getattr(acc, 'handled', False),
        })
    return JsonResponse(data, safe=False)


@csrf_exempt
def mark_alert_handled(request, hospital_id, accident_id):
    """
    API: Mark an accident alert as handled
    """
    hospital = get_object_or_404(Hospital, pk=hospital_id)
    acc = get_object_or_404(Accident, pk=accident_id, nearest_hospital=hospital)
    acc.handled = True
    acc.save()
    return JsonResponse({"status": "success", "accident_id": acc.id})


# ---------------------------
# Add Hospital (Admin) Views
# ---------------------------

class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['name', 'address', 'phone']  # adjust fields based on your model


def add_hospital(request):
    """
    Admin View: Add a new hospital
    """
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hospitalapp:add_hospital')  # or redirect to dashboard/list
    else:
        form = HospitalForm()
    return render(request, 'hospitalapp/add_hospital.html', {'form': form})


def hospital_api(request):
    """
    API: Return all hospitals as JSON (for map or alerts)
    """
    hospitals = Hospital.objects.all().values('id', 'name', 'address', 'phone', 'latitude', 'longitude')
    return JsonResponse(list(hospitals), safe=False)

import json

from django.shortcuts import render, get_object_or_404
from accounts.models import Hospital
from accidentapp.models import Accident
import json

def accident_map(request):
    # Fetch all accidents
    accidents = Accident.objects.all()
    accident_data = []
    for a in accidents:
        accident_data.append({
            'id': a.id,
            'location': a.location,
            'severity': a.severity,
            'latitude': a.latitude,
            'longitude': a.longitude,
            'time': a.time.strftime('%Y-%m-%d %H:%M:%S'),
            'handled': a.handled,
            'hospital': a.nearest_hospital.name if a.nearest_hospital else 'N/A'
        })

    # Fetch all hospitals
    hospitals = Hospital.objects.all()
    hospital_data = []
    for h in hospitals:
        hospital_data.append({
            'id': h.id,
            'name': h.name,
            'address': h.address,
            'phone': h.phone,
            'latitude': h.latitude,
            'longitude': h.longitude
        })

    context = {
        'accidents_json': json.dumps(accident_data),
        'hospitals_json': json.dumps(hospital_data)
    }

    return render(request, 'hospitalapp/accident_map.html', context)

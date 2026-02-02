from django.shortcuts import render, redirect
from .models import Accident
from .forms import AccidentForm

def accident_list(request):
    accidents = Accident.objects.all()
    return render(request, 'accidents/accident_list.html', {'accidents': accidents})

def add_accident(request):
    if request.method == 'POST':
        form = AccidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AccidentForm()
    return render(request, 'accidents/add_accident.html', {'form': form})

from django.http import JsonResponse

def get_accidents(request):
    accidents = Accident.objects.all().values(
        'id', 
        'latitude', 
        'longitude', 
        'severity', 
        'location'
    )
    return JsonResponse(list(accidents), safe=False)

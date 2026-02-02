from django import forms
from .models import Accident

class AccidentForm(forms.ModelForm):
    class Meta:
        model = Accident
        fields = ['location','severity','description','latitude','longitude']

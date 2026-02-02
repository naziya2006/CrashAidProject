from django.http import HttpResponse
from .firebase import send_firebase_alert

def send_alert(request):
    tokens = ["DEMO_TOKEN_123"]  # Dummy token for demo
    response = send_firebase_alert(
        title="🚨 CrashAid Demo Alert 🚨",
        body="Accident detected nearby (Demo)",
        tokens=tokens
    )
    return HttpResponse(f"Alert sent! Success: {response.success_count}")

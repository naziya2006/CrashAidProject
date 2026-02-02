from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Accident
from send_notification import send_accident_alert
from accounts.models import Hospital

@receiver(post_save, sender=Accident)
def send_alert_on_accident(sender, instance, created, **kwargs):
    if created:
        # Compose message
        title = "🚨 ACCIDENT ALERT 🚨"
        message = f"Accident ID: {instance.id}\nSeverity: {instance.severity}\nLocation: {instance.location}"

        # Fetch device tokens safely (only if field exists)
        registration_ids = []
        for hosp in Hospital.objects.all():
            if hasattr(hosp, 'device_token') and hosp.device_token:
                registration_ids.append(hosp.device_token)

        if registration_ids:
            result = send_accident_alert(device_tokens=registration_ids, title=title, message=message)
            print("Notification sent. Result:", result)
        else:
            print("No device tokens found for hospitals. Notification not sent.")

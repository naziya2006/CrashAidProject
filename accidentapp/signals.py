from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Accident
from firebase_admin import messaging

@receiver(post_save, sender=Accident)
def send_accident_notification(sender, instance, created, **kwargs):
    if created:
        # Create a notification message
        message = messaging.Message(
            notification=messaging.Notification(
                title="New Accident Reported!",
                body=f"Accident at {instance.location}",
            ),
            topic="accidents",  # or use `token="device_token"` if sending to single device
        )

        # Send the message via Firebase
        try:
            response = messaging.send(message)  # default app
            print("Successfully sent message:", response)
        except Exception as e:
            print("Error sending Firebase message:", e)

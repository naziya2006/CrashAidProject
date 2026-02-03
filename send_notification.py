import os
import firebase_admin
from firebase_admin import credentials, messaging

# Path to Render secret
firebase_key_path = "/etc/secrets/serviceAccountKey.json"

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_key_path)
    firebase_admin.initialize_app(cred)

def send_accident_alert(title, message, registration_ids):
    message_obj = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=message),
        tokens=registration_ids
    )
    try:
        response = messaging.send_each_for_multicast(message_obj)
        print(f"Sent: {response.success_count}, Failed: {response.failure_count}")
        if response.failure_count > 0:
            for resp, token in zip(response.responses, registration_ids):
                if not resp.success:
                    print(f"Failed token: {token}, error: {resp.exception}")
    except Exception as e:
        print("Error sending message:", e)

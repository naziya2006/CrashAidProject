import firebase_admin
from firebase_admin import credentials, messaging
import os

# Use Render secret path
FIREBASE_KEY_PATH = "/etc/secrets/serviceAccountKey.json"

cred = credentials.Certificate(FIREBASE_KEY_PATH)
firebase_admin.initialize_app(cred)

def send_firebase_alert(title, body, tokens):
    message = messaging.MulticastMessage(
        notification=messaging.Notification(title=title, body=body),
        tokens=tokens,
    )
    response = messaging.send_multicast(message)
    return response.success_count
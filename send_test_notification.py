# send_test_notification.py

import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase app with service account
cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Create a message to send
message = messaging.MulticastMessage(
    tokens=[
        "DEVICE_TOKEN_1",
        "DEVICE_TOKEN_2",
    ],
    notification=messaging.Notification(
        title="🚨 CrashAid Test Alert 🚨",
        body="This is a test notification from CrashAid"
    ),
)

# Send the message
response = messaging.send_multicast(message)
print(f"Successfully sent {response.success_count} messages, {response.failure_count} failures.")

import os
import firebase_admin
from firebase_admin import credentials, messaging

# Path to Render secret file
FIREBASE_KEY_PATH = "/etc/secrets/serviceAccountKey.json"

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred)

def send_accident_alert(title, message, registration_ids):
    """
    Send FCM notifications to multiple devices.
    registration_ids: list of FCM device tokens
    """
    message_obj = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=message
        ),
        tokens=registration_ids
    )

    try:
        response = messaging.send_each_for_multicast(message_obj)
        print(
            f"Successfully sent message: "
            f"{response.success_count} sent, {response.failure_count} failed"
        )

        if response.failure_count > 0:
            for resp, token in zip(response.responses, registration_ids):
                if not resp.success:
                    print(f"Failed token: {token}, error: {resp.exception}")

    except Exception as e:
        print("Error sending message:", e)


# Example usage (replace with real FCM tokens)
if __name__ == "__main__":
    registration_ids = [
        "YOUR_DEVICE_FCM_TOKEN_HERE"
    ]
    send_accident_alert(
        "🚨 Accident Alert 🚨",
        "This is a test accident message",
        registration_ids
    )
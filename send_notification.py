import firebase_admin
from firebase_admin import credentials, messaging

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

def send_accident_alert(title, message, registration_ids):
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


# Replace with actual FCM tokens
registration_ids = [
    "YOUR_DEVICE_FCM_TOKEN_HERE"
]

send_accident_alert(
    "🚨 Accident Alert 🚨",
    "Test accident message",
    registration_ids
)

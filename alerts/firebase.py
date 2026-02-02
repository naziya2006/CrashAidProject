import firebase_admin
from firebase_admin import credentials, messaging

# Firebase init (sirf ek baar)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

# alerts/firebase.py

def send_firebase_alert(title, body, tokens):
    """
    Dummy Firebase alert for demo purpose.
    Always returns success, no real notification sent.
    """
    if not tokens:
        return "No tokens provided"

    # Print demo info
    print(f"Demo Alert Sent! Title: {title}, Body: {body}, Tokens: {tokens}")

    # Return dummy success response
    class DummyResponse:
        success_count = len(tokens)
    return DummyResponse()

import requests
import time
import random

# Your local API endpoint
API_URL = "http://127.0.0.1:8000/api/accident/"

# Example locations in India (latitude, longitude)
locations = [
    ("Mumbai", 19.0760, 72.8777),
    ("Pune", 18.5204, 73.8567),
    ("Delhi", 28.6139, 77.2090),
    ("Bangalore", 12.9716, 77.5946),
    ("Hyderabad", 17.3850, 78.4867),
    ("Chennai", 13.0827, 80.2707),
]

severities = ["Low", "Medium", "High", "Critical"]

def send_accident():
    loc = random.choice(locations)
    severity = random.choice(severities)
    data = {
        "location": loc[0],
        "severity": severity,
        "latitude": loc[1] + random.uniform(-0.01, 0.01),  # slight variation
        "longitude": loc[2] + random.uniform(-0.01, 0.01)
    }
    try:
        response = requests.post(API_URL, json=data)
        print("Sent:", data, "| Response:", response.json())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    while True:
        send_accident()
        time.sleep(5)  # send every 5 seconds

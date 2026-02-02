# test_api_full.py
import requests
import json
import time

# IoT accident data
accidents = [
    {"location": "Pune Highway", "severity": "High", "hospital": "City Hospital"},
    {"location": "Mumbai Airport Road", "severity": "Low", "hospital": "City Hospital"},
    {"location": "Highway near Pune", "severity": "Critical", "hospital": "City Hospital"}
]

# Function to POST accident to Django API
def send_accident(acc):
    url = "http://127.0.0.1:8000/api/accident/"
    response = requests.post(url, json=acc)
    print(f"Sent: {acc['location']} | Response: {response.json()}")

# Add lat/lon using simple geocoding API
def geocode(location):
    try:
        response = requests.get(f"https://nominatim.openstreetmap.org/search?format=json&q={location}")
        data = response.json()
        if data and len(data) > 0:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print("Geocoding error:", e)
    return None, None

# Example nearest hospital coordinates
nearest_hospital = {
    "City Hospital": {"lat": 18.5204, "lon": 73.8567}
}

# Loop through accidents
for acc in accidents:
    lat, lon = geocode(acc["location"])
    acc["latitude"] = lat
    acc["longitude"] = lon
    hospital_coords = nearest_hospital.get(acc["hospital"])
    if hospital_coords:
        acc["nearest_hospital_lat"] = hospital_coords["lat"]
        acc["nearest_hospital_lon"] = hospital_coords["lon"]
    else:
        acc["nearest_hospital_lat"] = None
        acc["nearest_hospital_lon"] = None

    send_accident(acc)
    time.sleep(1)  # small delay between posts

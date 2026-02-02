import requests
import random
import time

# Correct API endpoints
ACCIDENT_API = "http://127.0.0.1:8000/accidentapp/api/accident/"
LATEST_API = "http://127.0.0.1:8000/accidentapp/api/latest_accidents/"
HOSPITAL_API = "http://127.0.0.1:8000/accidentapp/api/hospitals/"

# Sample locations and severity levels
locations = ["Pune Highway", "Mumbai Road", "Delhi Expressway", "Khopoli Junction"]
severities = ["Low", "Medium", "High", "Critical"]

print("=== Posting 5 test accidents ===")
for i in range(5):
    data = {
        "location": random.choice(locations),
        "severity": random.choice(severities),
        "description": "IoT detected accident"
    }

    try:
        res = requests.post(ACCIDENT_API, json=data)
        print(f"\nRequest {i+1}: Status Code {res.status_code}, URL: {res.url}")
        try:
            print("Response JSON:", res.json())
        except ValueError:
            print("Response is not JSON. Raw response:")
            print(res.text)
    except requests.exceptions.RequestException as e:
        print("Error connecting to API:", e)

    time.sleep(1)  # 1-second delay between posts

print("\n=== Fetching latest 5 accidents ===")
try:
    res = requests.get(LATEST_API)
    print("Status Code:", res.status_code)
    print("Response JSON:", res.json())
except requests.exceptions.RequestException as e:
    print("Error connecting to API:", e)

print("\n=== Fetching all hospitals ===")
try:
    res = requests.get(HOSPITAL_API)
    print("Status Code:", res.status_code)
    print("Response JSON:", res.json())
except requests.exceptions.RequestException as e:
    print("Error connecting to API:", e)

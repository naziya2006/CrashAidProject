import requests
import random
import time

URL = "http://127.0.0.1:8000/api/accident/"

LOCATIONS = [
    {"name":"Pune Highway","lat":18.59,"lon":73.78},
    {"name":"Pune Highway Near Wakad","lat":18.56,"lon":73.78},
    {"name":"Mumbai Airport Road","lat":19.09,"lon":72.87},
    {"name":"Highway near Pune","lat":18.53,"lon":73.82},
    {"name":"Delhi Expressway","lat":28.61,"lon":77.20},
    {"name":"Khopoli Junction","lat":18.67,"lon":73.44},
]

HOSPITALS = [
    {"id":1,"name":"City Hospital"},
    {"id":2,"name":"Mumbai Hospital"},
    {"id":3,"name":"Ruby Clinic"},
]

SEVERITIES = ["Low","Medium","High","Critical"]

DESCRIPTIONS = ["Car collision detected","Minor accident","High severity collision","IoT detected","Multiple vehicles"]

def post_accident():
    acc = random.choice(LOCATIONS)
    hosp = random.choice(HOSPITALS)
    data = {
        "location": acc["name"],
        "latitude": acc["lat"]+random.random()*0.01,
        "longitude": acc["lon"]+random.random()*0.01,
        "severity": random.choice(SEVERITIES),
        "hospital": hosp["name"],
        "description": random.choice(DESCRIPTIONS),
        "nearest_hospital": hosp["id"]
    }
    try:
        res = requests.post(URL,json=data)
        print(res.json())
    except Exception as e:
        print("Error:",e)

if __name__=="__main__":
    while True:
        post_accident()
        time.sleep(5)

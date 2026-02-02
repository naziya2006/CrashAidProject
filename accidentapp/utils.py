from accounts.models import Hospital
from math import radians, cos, sin, asin, sqrt

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1))*cos(radians(lat2))*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def find_nearest_hospital(acc_lat, acc_lon):
    hospitals = Hospital.objects.all()
    nearest = None
    min_dist = float('inf')
    for h in hospitals:
        dist = haversine(acc_lat, acc_lon, h.latitude, h.longitude)
        if dist < min_dist:
            min_dist = dist
            nearest = h
    return nearest

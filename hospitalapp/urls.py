from django.urls import path
from . import views

app_name = 'hospitalapp'  # namespacing the URLs

urlpatterns = [
    # Hospital Dashboard
    path('<int:hospital_id>/dashboard/', views.dashboard, name='dashboard'),

    # Latest accident alerts API
    path('<int:hospital_id>/alerts/', views.latest_accident_alerts, name='latest_accident_alerts'),

    # Mark an accident alert as handled
    path('<int:hospital_id>/alerts/<int:accident_id>/handle/', views.mark_alert_handled, name='mark_alert_handled'),

    # Add Hospital (Admin)
    path('add/', views.add_hospital, name='add_hospital'),

    # Hospital API (for map or alerts)
    path('api/', views.hospital_api, name='hospital_api'),

    # Accident map view inside hospital app
    path('accident_map/', views.accident_map, name='accident_map'),
]

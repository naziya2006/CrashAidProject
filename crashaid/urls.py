from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('accidentapp.urls')),  # ✅ HOME PAGE

    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accidentapp/', include('accidentapp.urls')),
    path('hospitalapp/', include('hospitalapp.urls')), 
    path('alerts/', include('alerts.urls')),

    # API URLs
    path('accidentapp/api/', include('accidentapp.api_urls')),
    path('hospitalapp/api/', include('hospitalapp.api_urls')),
]

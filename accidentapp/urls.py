from django.urls import path
from . import views
from .views import iot_accident

urlpatterns = [
    path('', views.accident_list, name='accident_list'),
    path('add/', views.add_accident, name='add_accident'),
    path('<int:pk>/', views.accident_detail, name='accident_detail'),
    path('map/', views.map_view, name='accident_map'),
    path('api/iot_accident/', iot_accident, name='iot_accident'),
]

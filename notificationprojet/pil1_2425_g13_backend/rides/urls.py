from django.urls import path
from . import views

urlpatterns = [
    path('accept/<int:ride_id>/', views.accept_ride, name='accept_ride'),
    path('reject/<int:ride_id>/', views.reject_ride, name='reject_ride'),
    path('notifications/', views.get_notifications, name='get_notifications'),
]
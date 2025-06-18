from django.db import models
from users.models import User

class Ride(models.Model):
    passenger = models.ForeignKey(User, related_name='passenger_rides', on_delete=models.CASCADE)
    driver = models.ForeignKey(User, related_name='driver_rides', on_delete=models.CASCADE, null=True, blank=True)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    ride_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride from {self.start_location} to {self.end_location} - Status: {self.ride_status}"
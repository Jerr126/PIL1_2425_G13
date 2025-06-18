from rest_framework import serializers
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

class PassengerRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'driver', 'status', 'pickup_location', 'dropoff_location', 'created_at']

class DriverRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'passenger', 'status', 'pickup_location', 'dropoff_location', 'created_at']
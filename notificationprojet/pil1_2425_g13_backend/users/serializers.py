from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']  # Assuming 'role' indicates passenger or driver

class PassengerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification  # Assuming Notification model exists
        fields = ['id', 'message', 'timestamp']  # Adjust fields as necessary

class DriverNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification  # Assuming Notification model exists
        fields = ['id', 'message', 'timestamp']  # Adjust fields as necessary

class MessagingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message  # Assuming Message model exists
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']  # Adjust fields as necessary
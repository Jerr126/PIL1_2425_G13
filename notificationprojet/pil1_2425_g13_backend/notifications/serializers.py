from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'notification_type', 'created_at']

    def validate(self, data):
        user = self.context['request'].user
        if user.role == 'passenger' and data['notification_type'] != 'passenger':
            raise serializers.ValidationError("Passengers can only see passenger notifications.")
        elif user.role == 'driver' and data['notification_type'] != 'driver':
            raise serializers.ValidationError("Drivers can only see driver notifications.")
        return data

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'mode', 'message', 'created_at']
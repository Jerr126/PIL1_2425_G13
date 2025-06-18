from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'timestamp']

    def validate(self, data):
        user = self.context['request'].user
        if user.role == 'passenger' and data['receiver'].role != 'driver':
            raise serializers.ValidationError("Passengers can only send messages to drivers.")
        if user.role == 'driver' and data['receiver'].role != 'passenger':
            raise serializers.ValidationError("Drivers can only send messages to passengers.")
        return data
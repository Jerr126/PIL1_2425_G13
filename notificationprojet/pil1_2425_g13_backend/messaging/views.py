from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from users.models import User

class MessageViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        if user.mode == 'passenger':
            messages = Message.objects.filter(receiver=user, sender__mode='driver')
        elif user.mode == 'driver':
            messages = Message.objects.filter(receiver=user, sender__mode='passenger')
        else:
            return Response({"detail": "Invalid user mode."}, status=400)

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        data = request.data

        if user.mode == 'passenger':
            if not data.get('receiver') or User.objects.get(id=data['receiver']).mode != 'driver':
                return Response({"detail": "Invalid receiver."}, status=400)
        elif user.mode == 'driver':
            if not data.get('receiver') or User.objects.get(id=data['receiver']).mode != 'passenger':
                return Response({"detail": "Invalid receiver."}, status=400)
        else:
            return Response({"detail": "Invalid user mode."}, status=400)

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, pk=None):
        message = get_object_or_404(Message, pk=pk)
        if message.sender != request.user and message.receiver != request.user:
            return Response({"detail": "Not found."}, status=404)
        serializer = MessageSerializer(message)
        return Response(serializer.data)
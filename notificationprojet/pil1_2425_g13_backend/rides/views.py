from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from .models import Ride, Notification
from .serializers import RideSerializer, NotificationSerializer
from users.models import User

class RideViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def accept_ride(self, request, pk=None):
        ride = get_object_or_404(Ride, pk=pk)
        user = request.user

        if user.role == 'driver':
            ride.status = 'accepted'
            ride.save()
            Notification.objects.create(user=ride.passenger, message=f"Your ride request has been accepted by {user.username}.")
            return Response({"message": "Ride accepted."}, status=200)
        return Response({"error": "Only drivers can accept rides."}, status=403)

    def reject_ride(self, request, pk=None):
        ride = get_object_or_404(Ride, pk=pk)
        user = request.user

        if user.role == 'driver':
            ride.status = 'rejected'
            ride.save()
            Notification.objects.create(user=ride.passenger, message=f"Your ride request has been rejected by {user.username}.")
            return Response({"message": "Ride rejected."}, status=200)
        return Response({"error": "Only drivers can reject rides."}, status=403)

class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        if user.role == 'passenger':
            notifications = Notification.objects.filter(user=user, type='passenger')
        elif user.role == 'driver':
            notifications = Notification.objects.filter(user=user, type='driver')
        else:
            return Response({"error": "Invalid user role."}, status=400)

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Logic for creating notifications can be added here if needed
        pass
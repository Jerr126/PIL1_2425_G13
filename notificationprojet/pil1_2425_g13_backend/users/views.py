from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Notification
from .serializers import UserSerializer, NotificationSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post'])
    def switch_mode(self, request, pk=None):
        user = self.get_object()
        if user.mode == 'passenger':
            user.mode = 'driver'
        else:
            user.mode = 'passenger'
        user.save()
        return Response({'mode': user.mode})

    @action(detail=True, methods=['get'])
    def notifications(self, request, pk=None):
        user = self.get_object()
        if user.mode == 'passenger':
            notifications = Notification.objects.filter(user=user, type='passenger')
        else:
            notifications = Notification.objects.filter(user=user, type='driver')
        
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def accept_request(self, request, pk=None):
        user = self.get_object()
        if user.mode == 'driver':
            # Logic to accept a ride request
            # Assuming there's a method to handle this
            # accept_ride_request(request.data)
            return Response({'status': 'request accepted'}, status=status.HTTP_200_OK)
        return Response({'error': 'Only drivers can accept requests'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def reject_request(self, request, pk=None):
        user = self.get_object()
        if user.mode == 'driver':
            # Logic to reject a ride request
            # Assuming there's a method to handle this
            # reject_ride_request(request.data)
            return Response({'status': 'request rejected'}, status=status.HTTP_200_OK)
        return Response({'error': 'Only drivers can reject requests'}, status=status.HTTP_403_FORBIDDEN)
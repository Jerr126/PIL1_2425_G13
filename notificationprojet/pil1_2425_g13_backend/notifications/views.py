from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from django.shortcuts import render

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notifications_list(request):
    mode = request.GET.get('mode')
    if mode not in ['passenger', 'driver']:
        return Response([], status=400)
    notifications = Notification.objects.filter(user=request.user, mode=mode).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)

def notifications_page(request):
    return render(request, 'notifications.html')
# ...existing code...
class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user
        if user.mode == 'passenger':
            notifications = Notification.objects.filter(user=user, type='passenger')
        elif user.mode == 'driver':
            notifications = Notification.objects.filter(user=user, type='driver')
        else:
            return Response({"detail": "Invalid user mode."}, status=400)

        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def accept_request(self, request, pk=None):
        notification = Notification.objects.get(pk=pk)
        if notification.type == 'passenger' and notification.driver == request.user:
            notification.status = 'accepted'
            notification.save()
            return Response({"detail": "Request accepted."})
        elif notification.type == 'driver' and notification.passenger == request.user:
            notification.status = 'accepted'
            notification.save()
            return Response({"detail": "Request accepted."})
        return Response({"detail": "You cannot accept this request."}, status=403)

    def reject_request(self, request, pk=None):
        notification = Notification.objects.get(pk=pk)
        if notification.type == 'passenger' and notification.driver == request.user:
            notification.status = 'rejected'
            notification.save()
            return Response({"detail": "Request rejected."})
        elif notification.type == 'driver' and notification.passenger == request.user:
            notification.status = 'rejected'
            notification.save()
            return Response({"detail": "Request rejected."})
        return Response({"detail": "You cannot reject this request."}, status=403)
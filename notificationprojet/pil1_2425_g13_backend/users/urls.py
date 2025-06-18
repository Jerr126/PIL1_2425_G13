from django.urls import path
from .views import UserModeView, NotificationListView

urlpatterns = [
    path('mode/', UserModeView.as_view(), name='user_mode'),
    path('notifications/', NotificationListView.as_view(), name='notification_list'),
]
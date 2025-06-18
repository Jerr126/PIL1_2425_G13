from django.urls import path
from .views import NotificationListView, NotificationDetailView
from .views import notifications_list, notifications_page
urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),
]

urlpatterns = [
    path('api/notifications/', notifications_list, name='notifications_list'),
    path('notifications/', notifications_page, name='notifications_page'),
]
from django.urls import path
from .views import MessageListView, MessageCreateView

urlpatterns = [
    path('messages/', MessageListView.as_view(), name='message-list'),
    path('messages/create/', MessageCreateView.as_view(), name='message-create'),
]

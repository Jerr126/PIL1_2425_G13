from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('conversation/<int:conversation_id>/', views.conversation, name='conversation'),
    path('start/<int:user_id>/', views.start_conversation, name='start_conversation'),
    path('send/<int:conversation_id>/', views.send_message, name='send_message'),
]
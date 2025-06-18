from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('rides/', include('rides.urls')),
    path('notifications/', include('notifications.urls')),
    path('messaging/', include('messaging.urls')),
]
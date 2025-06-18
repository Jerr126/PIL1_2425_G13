from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'created_at', 'is_read')
    list_filter = ('notification_type', 'is_read')
    search_fields = ('user__username', 'notification_type')

admin.site.register(Notification, NotificationAdmin)
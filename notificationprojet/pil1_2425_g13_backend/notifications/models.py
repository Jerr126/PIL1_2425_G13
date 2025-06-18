from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    MODE_CHOICES = [
        ('passenger', 'Passager'),
        ('driver', 'Conducteur'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('request', 'Request'),
        ('accept', 'Accept'),
        ('reject', 'Reject'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.created_at}"
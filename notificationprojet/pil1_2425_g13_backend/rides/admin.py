from django.contrib import admin
from .models import Ride

class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'passenger', 'driver', 'status', 'created_at')
    search_fields = ('passenger__username', 'driver__username', 'status')
    list_filter = ('status',)

admin.site.register(Ride, RideAdmin)
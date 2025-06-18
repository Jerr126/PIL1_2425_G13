from django.test import TestCase
from django.urls import reverse
from notifications.models import Notification
from users.models import User

class NotificationTests(TestCase):

    def setUp(self):
        self.passenger = User.objects.create_user(username='passenger', password='pass123', role='passenger')
        self.driver = User.objects.create_user(username='driver', password='driver123', role='driver')
        self.notification_passenger = Notification.objects.create(user=self.passenger, message='Your ride request has been accepted.', notification_type='ride_accepted')
        self.notification_driver = Notification.objects.create(user=self.driver, message='You have a new ride request.', notification_type='new_request')

    def test_passenger_notifications(self):
        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('notifications:list'))
        self.assertContains(response, 'Your ride request has been accepted.')
        self.assertNotContains(response, 'You have a new ride request.')

    def test_driver_notifications(self):
        self.client.login(username='driver', password='driver123')
        response = self.client.get(reverse('notifications:list'))
        self.assertContains(response, 'You have a new ride request.')
        self.assertNotContains(response, 'Your ride request has been accepted.')

    def test_no_access_to_other_role_notifications(self):
        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('notifications:list'))
        self.assertNotContains(response, 'You have a new ride request.')

        self.client.login(username='driver', password='driver123')
        response = self.client.get(reverse('notifications:list'))
        self.assertNotContains(response, 'Your ride request has been accepted.')
from django.test import TestCase
from django.urls import reverse
from .models import User, Notification

class UserModelTests(TestCase):

    def setUp(self):
        self.passenger = User.objects.create_user(username='passenger', password='pass123', role='passenger')
        self.driver = User.objects.create_user(username='driver', password='driver123', role='driver')

    def test_user_creation(self):
        self.assertEqual(self.passenger.username, 'passenger')
        self.assertEqual(self.driver.role, 'driver')

class NotificationTests(TestCase):

    def setUp(self):
        self.passenger = User.objects.create_user(username='passenger', password='pass123', role='passenger')
        self.driver = User.objects.create_user(username='driver', password='driver123', role='driver')
        self.notification = Notification.objects.create(user=self.passenger, message='Ride request sent', type='passenger')

    def test_passenger_notifications(self):
        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('notifications:passenger_notifications'))
        self.assertContains(response, 'Ride request sent')

    def test_driver_notifications(self):
        self.client.login(username='driver', password='driver123')
        response = self.client.get(reverse('notifications:driver_notifications'))
        self.assertNotContains(response, 'Ride request sent')

class MessagingTests(TestCase):

    def setUp(self):
        self.passenger = User.objects.create_user(username='passenger', password='pass123', role='passenger')
        self.driver = User.objects.create_user(username='driver', password='driver123', role='driver')

    def test_messaging_access(self):
        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('messaging:chat', args=[self.driver.id]))
        self.assertEqual(response.status_code, 403)  # Passenger should not access driver chat

        self.client.login(username='driver', password='driver123')
        response = self.client.get(reverse('messaging:chat', args=[self.passenger.id]))
        self.assertEqual(response.status_code, 403)  # Driver should not access passenger chat

    def test_messaging_after_acceptance(self):
        # Simulate acceptance of ride request
        self.passenger.accepted = True
        self.passenger.save()

        self.client.login(username='driver', password='driver123')
        response = self.client.get(reverse('messaging:chat', args=[self.passenger.id]))
        self.assertEqual(response.status_code, 200)  # Driver can access chat after acceptance

        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('messaging:chat', args=[self.driver.id]))
        self.assertEqual(response.status_code, 200)  # Passenger can access chat after acceptance
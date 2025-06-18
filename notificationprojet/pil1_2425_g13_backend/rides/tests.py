from django.test import TestCase
from django.urls import reverse
from users.models import User
from rides.models import Ride
from notifications.models import Notification

class RideTests(TestCase):

    def setUp(self):
        self.passenger = User.objects.create_user(username='passenger', password='pass123', role='passenger')
        self.driver = User.objects.create_user(username='driver', password='driver123', role='driver')
        self.ride = Ride.objects.create(passenger=self.passenger, driver=self.driver, status='pending')

    def test_passenger_can_see_notifications(self):
        Notification.objects.create(user=self.passenger, message='Your ride request has been accepted.', ride=self.ride)
        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('notifications:list'))
        self.assertContains(response, 'Your ride request has been accepted.')

    def test_driver_can_see_notifications(self):
        Notification.objects.create(user=self.driver, message='You have a new ride request.', ride=self.ride)
        self.client.login(username='driver', password='driver123')
        response = self.client.get(reverse('notifications:list'))
        self.assertContains(response, 'You have a new ride request.')

    def test_passenger_cannot_access_driver_notifications(self):
        Notification.objects.create(user=self.driver, message='You have a new ride request.', ride=self.ride)
        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('notifications:list'))
        self.assertNotContains(response, 'You have a new ride request.')

    def test_driver_cannot_access_passenger_notifications(self):
        Notification.objects.create(user=self.passenger, message='Your ride request has been accepted.', ride=self.ride)
        self.client.login(username='driver', password='driver123')
        response = self.client.get(reverse('notifications:list'))
        self.assertNotContains(response, 'Your ride request has been accepted.')

    def test_driver_can_accept_ride(self):
        self.client.login(username='driver', password='driver123')
        response = self.client.post(reverse('rides:accept', args=[self.ride.id]))
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, 'accepted')
        self.assertEqual(response.status_code, 200)

    def test_driver_can_reject_ride(self):
        self.client.login(username='driver', password='driver123')
        response = self.client.post(reverse('rides:reject', args=[self.ride.id]))
        self.ride.refresh_from_db()
        self.assertEqual(self.ride.status, 'rejected')
        self.assertEqual(response.status_code, 200)

    def test_passenger_can_chat_with_driver_after_acceptance(self):
        self.client.login(username='driver', password='driver123')
        self.client.post(reverse('rides:accept', args=[self.ride.id]))
        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('messaging:chat', args=[self.driver.id]))
        self.assertEqual(response.status_code, 200)

    def test_passenger_cannot_chat_with_driver_if_rejected(self):
        self.client.login(username='driver', password='driver123')
        self.client.post(reverse('rides:reject', args=[self.ride.id]))
        self.client.login(username='passenger', password='pass123')
        response = self.client.get(reverse('messaging:chat', args=[self.driver.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden access

    def test_driver_cannot_chat_with_passenger_if_rejected(self):
        self.client.login(username='driver', password='driver123')
        self.client.post(reverse('rides:reject', args=[self.ride.id]))
        response = self.client.get(reverse('messaging:chat', args=[self.passenger.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden access
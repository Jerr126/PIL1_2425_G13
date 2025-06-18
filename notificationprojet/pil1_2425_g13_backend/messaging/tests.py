from django.test import TestCase
from django.urls import reverse
from users.models import User
from messaging.models import Message

class MessagingTests(TestCase):
    def setUp(self):
        self.passenger = User.objects.create_user(username='passenger', password='pass123', role='passenger')
        self.driver = User.objects.create_user(username='driver', password='driver123', role='driver')
        self.message_url = reverse('messaging:message')  # Assuming you have a URL named 'message'

    def test_passenger_can_send_message_to_driver(self):
        self.client.login(username='passenger', password='pass123')
        response = self.client.post(self.message_url, {'recipient_id': self.driver.id, 'content': 'Hello Driver!'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Message.objects.filter(sender=self.passenger, recipient=self.driver, content='Hello Driver!').exists())

    def test_driver_can_send_message_to_passenger(self):
        self.client.login(username='driver', password='driver123')
        response = self.client.post(self.message_url, {'recipient_id': self.passenger.id, 'content': 'Hello Passenger!'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Message.objects.filter(sender=self.driver, recipient=self.passenger, content='Hello Passenger!').exists())

    def test_passenger_cannot_send_message_when_driver_rejects(self):
        self.client.login(username='driver', password='driver123')
        # Simulate driver rejecting the ride request
        # Assuming you have a method to reject a ride request
        # self.driver.reject_ride_request(self.passenger)

        self.client.logout()
        self.client.login(username='passenger', password='pass123')
        response = self.client.post(self.message_url, {'recipient_id': self.driver.id, 'content': 'Can we talk?'})
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_driver_cannot_send_message_when_passenger_rejects(self):
        self.client.login(username='passenger', password='pass123')
        # Simulate passenger rejecting the ride request
        # Assuming you have a method to reject a ride request
        # self.passenger.reject_ride_request(self.driver)

        self.client.logout()
        self.client.login(username='driver', password='driver123')
        response = self.client.post(self.message_url, {'recipient_id': self.passenger.id, 'content': 'Can we talk?'})
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_passenger_can_only_see_driver_messages(self):
        self.client.login(username='passenger', password='pass123')
        self.client.post(self.message_url, {'recipient_id': self.driver.id, 'content': 'Hello Driver!'})
        response = self.client.get(reverse('messaging:inbox'))  # Assuming you have an inbox URL
        self.assertContains(response, 'Hello Driver!')
        self.assertNotContains(response, 'Hello Passenger!')

    def test_driver_can_only_see_passenger_messages(self):
        self.client.login(username='driver', password='driver123')
        self.client.post(self.message_url, {'recipient_id': self.passenger.id, 'content': 'Hello Passenger!'})
        response = self.client.get(reverse('messaging:inbox'))  # Assuming you have an inbox URL
        self.assertContains(response, 'Hello Passenger!')
        self.assertNotContains(response, 'Hello Driver!')
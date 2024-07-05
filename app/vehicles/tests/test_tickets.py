"""
API Vehicles, tickets tests.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import User, Police, Vehicle, Ticket


class TicketCreateAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.police_user = User.objects.create_user(
            email='police@example.com',
            password='password123',
            name='Test Police',
            role='police'
        )
        self.police = Police.objects.create(
            user=self.police_user,
            plate_num='123456'
        )
        self.regular_user = User.objects.create_user(
            email='user@example.com',
            password='password123',
            name='Regular User',
            role='user'
        )
        self.vehicle = Vehicle.objects.create(
            owner=self.regular_user,
            license_plate='ABC123',
            brand='Toyota',
            color='Rojo'
        )

    def test_create_ticket_as_police(self):
        self.client.force_authenticate(user=self.police_user)
        payload = {
            "placa_patente": "ABC123",
            "timestamp": "2023-06-29T12:34:56Z",
            "comentarios": "Texto libre"
        }
        url = reverse('create-ticket')
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(Ticket.objects.get().description, 'Texto libre')

    def test_create_ticket_as_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        payload = {
            "placa_patente": "ABC123",
            "timestamp": "2023-06-29T12:34:56Z",
            "comentarios": "Texto libre"
        }
        url = reverse('create-ticket')
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Ticket.objects.count(), 0)

    def test_create_ticket_with_nonexistent_vehicle(self):
        self.client.force_authenticate(user=self.police_user)
        payload = {
            "placa_patente": "NONEXISTENT123",
            "timestamp": "2023-06-29T12:34:56Z",
            "comentarios": "Texto libre"
        }
        url = reverse('create-ticket')
        response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Ticket.objects.count(), 0)

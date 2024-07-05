"""
Tests for report API
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Police, Vehicle, Ticket

User = get_user_model()


class ReportTicketAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='user@example.com',
            password='password123',
            name='Regular User',
            role='user'
        )
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
        self.vehicle = Vehicle.objects.create(
            owner=self.user,
            license_plate='ABC123',
            brand='Toyota',
            color='Rojo'
        )
        self.ticket = Ticket.objects.create(
            car=self.vehicle,
            police=self.police,
            description='Speeding',
            date='2023-06-29T12:34:56Z'
        )

    def test_ticket_report(self):
        url = reverse('ticket-report')
        res = self.client.get(
            url, {'email': 'user@example.com'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['comentarios'], 'Speeding')
        self.assertEqual(res.data[0]['placa_patente'], 'ABC123')

    def test_ticket_report_user_not_found(self):
        url = reverse('ticket-report')
        res = self.client.get(
            url, {'email': 'nonexistent@example.com'}, format='json')

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data['message'],
                         'User with this email does not exist.')

    def test_ticket_report_no_email_provided(self):
        url = reverse('ticket-report')
        res = self.client.get(url, {}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['message'],
                         'Email parameter is required.')

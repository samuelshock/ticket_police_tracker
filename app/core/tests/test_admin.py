"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


User = get_user_model()


class AdminSiteTest(TestCase):
    """Tests for Django admin."""

    def setUp(self) -> None:
        """Create user and client."""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123',
            role='user'
        )
        self.police = User.objects.create_user(
            email='policia@example.com',
            password='password123',
            role='police'
        )
        return super().setUp()

    def test_users_list(self):
        """Test that users are listed on page."""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.police.name)
        self.assertContains(res, self.police.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Change user')

    def test_create_user_page(self):
        """Test the create user page work."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Add user')

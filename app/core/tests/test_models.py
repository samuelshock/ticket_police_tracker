"""
Tests for the Django models modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


USER_ROLES = (
    'admin',
    'user',
    'police',
)


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


def create_police(email='user@example.com', password='testpass123'):
    """Create and return a new police user."""
    return get_user_model().objects.create_user(email, password, role='police')


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.role, USER_ROLES[1])

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.Com', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without en email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test create superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, USER_ROLES[0])

    def test_create_police_user(self):
        """Test create police user."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'test123',
            role=USER_ROLES[2]
        )
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, USER_ROLES[2])

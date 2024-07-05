"""
Tests for the Django models modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Police, Vehicle, Ticket


USER_ROLES = (
    'admin',
    'user',
    'police',
)


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


def create_police(email='police@example.com', password='testpolicepass123'):
    """Create and return a new police user."""
    police_user = get_user_model().objects.create_user(
        email, password, role='police')
    return Police.objects.create(user=police_user, plate_num='ABC123')


def create_vehicle(user, license_plate='123QWE', brand='Honda', color='black'):
    """Create and return a new vehicle."""
    return Vehicle.objects.create(
        owner=user,
        license_plate=license_plate,
        brand=brand,
        color=color)


class ModelTests(TestCase):
    """Test Models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = create_user(
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
            user = create_user(email, 'sample123')
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


class ModelTestsWithUser(TestCase):
    """Test Models with users."""

    def setUp(self) -> None:
        """Create user and police."""
        self.user = create_user()
        self.police = create_police()
        return super().setUp()

    def test_create_vehicle(self):
        """Test create a new vehicle."""
        data = {
            'owner': self.user,
            'license_plate': 'test123',
            'brand': 'toyota',
            'color': 'white'
        }
        vehicle = Vehicle.objects.create(**data)

        self.assertEqual(vehicle.owner.id, self.user.id)
        self.assertEqual(vehicle.license_plate, data['license_plate'])
        self.assertEqual(vehicle.brand, data['brand'])
        self.assertEqual(vehicle.color, data['color'])

    def test_create_ticket(self):
        """Test create a new ticket"""
        data = {
            'police': self.police,
            'car': create_vehicle(self.user),
            'description': 'Test ticket'
        }

        ticket = Ticket.objects.create(**data)

        self.assertEqual(ticket.police.id, data['police'].id)
        self.assertEqual(ticket.car.id, data['car'].id)
        self.assertEqual(ticket.description, data['description'])

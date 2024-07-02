"""
Core Models.
"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(
            email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        if user.role == 'police':
            user.is_staff = True

        if user.role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'admin'
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    USER_ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('police', 'Police'),
    )
    role = models.CharField(
        max_length=10, choices=USER_ROLES, default='user')
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        permissions = [
            ("can_manage_all", "Can manage all"),
        ]


class Police(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='police_profile')
    plate_num = models.CharField(max_length=20)


class Vehicle(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='autos')
    license_plate = models.CharField(max_length=20)
    brand = models.CharField(max_length=50)
    color = models.CharField(max_length=30)


class Ticket(models.Model):
    police = models.ForeignKey(
        Police, on_delete=models.CASCADE, related_name='infracciones')
    car = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='infracciones')
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

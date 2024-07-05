"""
Custom forms for models
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User, Police, Vehicle


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'name', 'password1', 'password2', 'role')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'role', 'is_staff', 'is_active')


class PoliceCreationForm(forms.ModelForm):
    class Meta:
        model = Police
        fields = ('user', 'plate_num')


class PoliceChangeForm(forms.ModelForm):
    class Meta:
        model = Police
        fields = ('user', 'plate_num')


class VehicleCreationForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('owner', 'license_plate', 'brand', 'color')


class VehicleChangeForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ('owner', 'license_plate', 'brand', 'color')

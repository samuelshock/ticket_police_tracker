"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Ticket, User, Police, Vehicle
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    PoliceCreationForm,
    PoliceChangeForm,
    VehicleChangeForm,
    VehicleCreationForm,
)


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Role', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'name',
                'password1',
                'password2',
                'role',
                'is_staff',
                'is_active'
            )}
         ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)


class PoliceAdmin(admin.ModelAdmin):
    add_form = PoliceCreationForm
    form = PoliceChangeForm
    model = Police
    list_display = ('user', 'plate_num')
    search_fields = ('user__email', 'plate_num')


class VehicleAdmin(admin.ModelAdmin):
    add_form = VehicleCreationForm
    form = VehicleChangeForm
    model = Vehicle
    list_display = ('license_plate', 'brand', 'color', 'user')
    search_fields = ('license_plate', 'brand', 'color', 'user__name')
    list_filter = ('brand', 'color')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('description', 'police', 'car', 'date')
    search_fields = ('description', 'police__user__name', 'car__license_plate')
    list_filter = ('date', 'police', 'car')
    ordering = ('-date',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Police, PoliceAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Ticket, TicketAdmin)

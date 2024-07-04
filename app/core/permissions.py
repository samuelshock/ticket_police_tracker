"""
API core permissions base.
"""
from rest_framework import permissions


class IsPolice(permissions.BasePermission):
    """
    Custom permission to only allow users with the police role.
    """

    def has_permission(self, request, view):
        return request.user\
            and request.user.is_authenticated\
            and request.user.role == 'police'

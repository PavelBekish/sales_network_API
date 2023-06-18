from django.contrib.auth.models import User
from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        employees = User.objects.filter(network_objects__id=obj.id)
        return request.user in employees

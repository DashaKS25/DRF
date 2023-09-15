from rest_framework import permissions


class IsOwnerOrCreate(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            return bool(request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='author').exists()))
        if request.method == "GET":
            return request.user.is_authenticated


class IsLoggedInPermission(permissions.BasePermission):
    """
    Custom permission to allow access to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Allow Django superusers
        if request.user.is_superuser:
            return True

        # Allow users in the "admin" group
        return request.user.groups.filter(name="admin").exists()

class IsDispatcher(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="dispatcher").exists()

class IsAdminOrDispatcher(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_superuser or
                request.user.groups.filter(name="dispatcher").exists() or
                request.user.groups.filter(name="admin").exists()
                )

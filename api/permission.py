from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Allow Django superusers
        if request.user.is_superuser:
            return True

        # Allow users in the "admin" group
        return request.user.groups.filter(name="admin").exists()

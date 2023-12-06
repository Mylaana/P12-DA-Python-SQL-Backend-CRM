from rest_framework import permissions

class UserProfilePermission(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.id == request.user.id:
            return True
        
        if request.user.team.name == 'gestion':
            return True

        return False

class TeamPermisison(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.user.is_admin:
            return True

        return False

class ClientPermisison(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.team.name == 'commerciale' and obj.ee_contact.id == request.user.id:
            return True

        return False

class ContractPermisison(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.team.name == 'gestion':
            return True

        if request.user.team.name == 'commerciale' and obj.client.ee_contact.id == request.user.id:
            return True

        return False

class EventPermisison(permissions.BasePermission):
    """Allow user to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own profile"""
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.team.name == 'gestion':
            return True

        if (request.method == 'POST' and
            request.user.team.name == 'commerciale' and 
                obj.contract.client.ee_contact.id == request.user.id):
            return True

        if (request.method in ['GET']  and
            request.user.team.name == 'support'):
            return True

        return False

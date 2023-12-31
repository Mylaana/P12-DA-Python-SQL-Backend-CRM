from rest_framework import permissions

class UserProfilePermission(permissions.BasePermission):
    """Object permission management"""

    def has_object_permission(self, request, view, obj):
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
    """Object permission management"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        return False

class ClientPermisison(permissions.BasePermission):
    """Object permission management"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.team.name == 'commerciale' and obj.ee_contact.id == request.user.id:
            return True

        return False

class ContractPermisison(permissions.BasePermission):
    """Object permission management"""

    def has_object_permission(self, request, view, obj):
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
    """Object permission management"""

    def has_permission(self, request, view):
        """
        method related permission management for events
        """
        if request.user.is_admin:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if (request.method in ['POST']  and
            request.user.team.name == 'commerciale'):
            return True

        if (request.method in ['PUT', 'PATCH']  and
            request.user.team.name == 'support'):
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        object related permission management for events
        """
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

        if (request.method in  ['PUT','PATCH'] and
            request.user.team.name == 'support' and
                obj.ee_contact.id == request.user.id):
            return True

        return False

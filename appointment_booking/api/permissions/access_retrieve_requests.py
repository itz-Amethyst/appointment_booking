from rest_framework.permissions import BasePermission

class Access_Retrieve_Permission(BasePermission):
    """
    Custom permission to require authentication only for PUT and POST requests.
    """

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated
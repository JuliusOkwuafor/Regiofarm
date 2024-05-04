from rest_framework.permissions import BasePermission


class IsUserORAdmin(BasePermission):
    """Allow access only to authenticated users or admin"""

    def has_permission(self, request, view):
        # Write permissions are only allowed for the owner of the snippet
        if request.method in ["POST", "PUT", "PATCH"]:
            return request.user and request.user.is_staff
        else:  # GET, HEAD, OPTIONS
            return True

    def has_object_permission(self, request, view, obj):
        # Read permission is granted if user is authenticated and owns the object,
        # otherwise read-only access (GET) is allowed
        return obj == request.user or request.user.is_staff


class IsSellerORRead(BasePermission):
    """Allow access only to authenticated seller"""

    def has_permission(self, request, view):
        # Write permissions are only allowed for the owner of the snippet
        if request.method in ["POST", "PUT", "PATCH"]:
            return request.user.role == "seller"
        else:  # GET, HEAD, OPTIONS
            return True

    def has_object_permission(self, request, view, obj):
        # Read permission is granted if user is authenticated and owns the object,
        # otherwise read-only access (GET) is allowed
        return obj.user == request.user or request.user.is_staff

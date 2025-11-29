from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Object owner can edit, others can only read
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for owner
        return obj.author == request.user

class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Only moderators and admins can create/edit
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.is_authenticated and (
            request.user.is_moderator or request.user.is_superuser
        )

class CanModerateContent(permissions.BasePermission):
    """
    Moderators can edit any content except other moderators'/admins'
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        
        # Admins can do anything
        if user.is_superuser:
            return True
        
        # Owner can edit their own content
        if hasattr(obj, 'author') and obj.author == user:
            return True
        
        # Moderators can edit content, but not other moderators'/admins'
        if user.is_moderator:
            if hasattr(obj, 'author'):
                author = obj.author
                # Cannot modify moderator or admin content
                if author.is_moderator or author.is_superuser:
                    return False
            return True
        
        return False

class IsProUser(permissions.BasePermission):
    """
    Only Pro users and above can access
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_pro or 
            request.user.is_moderator or 
            request.user.is_superuser
        )
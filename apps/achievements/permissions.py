from rest_framework import permissions

class AchievementPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_admin
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.available or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            return request.user.is_admin
        elif view.action == 'destroy':
            return request.user.is_admin
        else:
            return False
        
class AchievementGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_admin
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif view.action in ['update', 'partial_update']:
            return request.user.is_admin
        elif view.action == 'destroy':
            return request.user.is_admin
        else:
            return False
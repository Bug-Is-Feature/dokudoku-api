import json
from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_admin
        elif view.action in ['retrieve', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj == request.user or request.user.is_admin
        elif view.action == 'partial_update':
            body = json.loads(request.body)
            if 'uid' in body.keys():
                self.message = 'UID are not editable'
                return False
            if 'is_admin' in body.keys():
                return request.user.is_admin
            return obj == request.user or request.user.is_admin
        elif view.action == 'destroy':
            return request.user.is_admin
        else:
            return False
        
class UserAchievementPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            body = json.loads(request.body)
            if 'uid' in body.keys():
                return body['uid'] == str(request.user) or request.user.is_admin
            else:
                self.message = 'uid attribute is missing.'
                return False
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.user == request.user or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            return request.user.is_admin
        elif view.action == 'destroy':
            return request.user.is_admin
        else:
            return False
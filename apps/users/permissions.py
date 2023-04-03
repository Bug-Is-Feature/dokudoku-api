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
        elif view.action == 'update':
            self.message = 'Method PUT is not allowed, please use PATCH instead.'
            return False
        elif view.action == 'partial_update':
            body = json.loads(request.body)
            if 'uid' in body.keys():
                self.message = 'UID are not editable'
                return False
            if 'is_admin' in body.keys():
                if request.user.is_admin:
                    self.message = 'Use path `/user-admin` instead of `/users` to update admin status.'
                return False
            return obj == request.user or request.user.is_admin
        elif view.action == 'destroy':
            if obj.is_admin:
                self.message = 'Use path `/user-admin` instead of `/users` to delete admin account.'
                return False
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
        
class UserAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_admin
        elif view.action in ['retrieve', 'partial_update', 'destroy']:
            return request.user.is_admin
        else:
            return False
        
    def has_object_permission(self, request, view, obj):
        
        if view.action == 'retrieve':
            return request.user.is_admin
        elif view.action == 'update':
            self.message = 'Method PUT is not allowed, please use PATCH instead.'
            return False
        elif view.action == 'partial_update':
            body = json.loads(request.body)
            if len(body.keys()) > 1 or 'is_admin' not in body.keys():
                self.message = 'Only `is_admin` attribute is allowed, to update user data user `/users` path instead.'
                return False
            return request.user.is_admin
        elif view.action == 'destroy':
            if obj == request.user:
                self.message = 'Self delete is not allowed.'
                return False
            return request.user.is_admin
        else:
            return False
        
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
            if 'uid' in body:
                self.message = 'UID are not editable'
                return False
            if 'is_admin' in body:
                return request.user.is_admin
            return obj == request.user or request.user.is_admin
        elif view.action == 'destroy':
            return request.user.is_admin
        else:
            return False
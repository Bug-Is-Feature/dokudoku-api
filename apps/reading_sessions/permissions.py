import json
from rest_framework import permissions

class SessionPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if view.action == 'list':
            params = request.GET.copy()
            if 'owner' in params.keys():
                self.message = f"You do not have permission to view reading sessions of user: {params['owner']}"
                return params['owner'] == str(request.user) or request.user.is_admin
            else:
                return True
        elif view.action == 'create':
            body = json.loads(request.body)
            self.message = f'You do not have permission to create session for user: {body["uid"]}'
            return body['uid'] == str(request.user) or request.user.is_admin
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.created_by == request.user or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            return request.user.is_admin
        elif view.action == 'destroy':
            return request.user.is_admin
        else:
            return False
import json
from rest_framework import permissions

class BookPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            params = request.GET.copy()
            if 'owner' in params.keys():
                self.message = f'You do not have permission to view custom book of user: {params["owner"]}'
                return params['owner'] == str(request.user) or request.user.is_admin
            else:
                return True
        elif view.action == 'create':
            body = json.loads(request.body)
            if 'uid' in body.keys() and 'google_book_id' in body.keys():
                self.message = 'Request body with google_book_id and uid is not allowed, only one attribute can exist.'
                return False
            if 'uid' in body.keys():
                self.message = f'You do not have permission to create book for user: {body["uid"]}'
                return body['uid'] == str(request.user) or request.user.is_admin
            else:
                return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            params = request.GET.copy()
            if 'ggbookid' in params.keys():
                return True
            else:
                return obj.created_by == request.user or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            body = json.loads(request.body)
            if 'uid' in body.keys():
                return request.user.is_admin
            return obj.created_by == request.user or request.user.is_admin
        elif view.action == 'destroy':
            return obj.created_by == request.user or request.user.is_admin
        else:
            return False

class AuthorPermission(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_admin
        elif view.action == 'create':
            return True
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.book.google_book_id or obj.book.created_by == request.user or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            if obj.book.google_book_id:
                return request.user.is_admin
            return obj.book.created_by == request.user or request.user.is_admin
        elif view.action == 'destroy':
            return obj.book.created_by == request.user or request.user.is_admin
        else:
            return False
            
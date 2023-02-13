import json
from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import Library

class LibraryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            params = request.GET.copy()
            if 'uid' in params.keys():
                self.message = f'You do not have permission to view library of user: {params["user"]}'
                return params['uid'] == str(request.user) or request.user.is_admin
            else:
                return True
        elif view.action == 'create':
            return request.user.is_admin
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

class LibraryBookPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            params = request.GET.copy()
            if 'library_id' in params.keys():
                library_owner = get_object_or_404(Library.objects.filter(id=params['library_id']))
                self.message = 'You do not have permission to view books in other user\'s library'
                return library_owner == str(request.user) or request.user.is_admin
            else:
                return True
        elif view.action == 'create':
            body = json.loads(request.body)
            if 'book_data' in body.keys():
                book_owner = body['book_data']['created_by']
                if  book_owner and book_owner != str(request.user):
                    self.message = 'You can not add other user\'s custom book into your library.'
                    return request.user.is_admin
                else:
                    return True
            else:
                self.message = 'book_data attribute is missing.'
                return False
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return obj.library.created_by == request.user or request.user.is_admin
        elif view.action in ['update', 'partial_update']:
            body = json.loads(request.body)
            if 'is_completed' in body.keys():
                return obj.library.created_by == request.user or request.user.is_admin
            else:
                self.message = 'You do not have permission to edit this attribute'
                return request.user.is_admin
        elif view.action == 'destroy':
            return obj.library.created_by == request.user or request.user.is_admin
        else:
            return False
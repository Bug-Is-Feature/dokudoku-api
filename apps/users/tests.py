import uuid

from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from .models import User
from .views import UserViewSet

class TestSetUp(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin@admin.com'
        )
        self.user = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user@user.com',
        )

class UserViewSetTest(TestSetUp):
    
    def test_user_viewset_admin(self):
        '''
        Simulate an admin trying to fetch all users in the system

        All users in the database should show up
        '''
        request = self.factory.get('/api/users/')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 2,
            f'Expected 2 users from admin view, not {len(response.data)}.')

    def test_user_viewset_user(self):
        '''
        Simulate a user trying to fetch all users in the system
        but fetching all users is a privilege for admin

        An error message should return as response
        '''
        request = self.factory.get('/api/users/')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_user_path_param(self):
        '''
        Simulate a user/admin trying to retrieve user data 
        by passing :id as path parameter

        A response should return with specific user data
        '''
        request = self.factory.get(f'/api/users/{self.admin.uid}/')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'get': 'retrieve'})(request, pk=self.admin.uid)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['email'], 'admin@admin.com',
            f'Expected `admin@admin.com` as title, not `{response.data["email"]}`.')

    def test_user_path_param_no_permission(self):
        '''
        Simulate a user trying to retrieve other user's data 
        by passing :id of that user as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/users/{self.admin.uid}/')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'get': 'retrieve'})(request, pk=self.admin.uid)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_user_update(self):
        '''
        Simulate a user/admin trying to edit a user data

        A response should return with edited user data
        '''
        request = self.factory.put(f'/api/users/{self.admin.uid}/', {
            "email": "edited@edited.com"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'put': 'partial_update'})(request, pk=self.admin.uid)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['email'], 'edited@edited.com',
            f'Expected `edited@edited.com` as email, not `{response.data["email"]}`.')

    def test_user_update_no_permission(self):
        '''
        Simulate a user trying to edit other user's data
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.put(f'/api/users/{self.admin.uid}/', {
            "email": "edited@edited.com"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'put': 'partial_update'})(request, pk=self.admin.uid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 200, not {response.status_code}.')

    def test_user_delete(self):
        '''
        Simulate an admin trying to delete a user

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/users/{self.user.uid}/')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'delete': 'destroy'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(User.objects.filter(uid=self.user.uid).exists(), 
            f'Expected no user with uid `{self.user.uid}` still exist.')

    def test_user_delete_no_permission(self):
        '''
        Simulate a user trying to delete other user
        but deleting user is a privilege for admin

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/users/{self.user.uid}/')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'delete': 'destroy'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
            
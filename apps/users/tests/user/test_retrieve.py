from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...views import UserViewSet

class UserRetrieveTest(UsersAppTestSetUp):

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
            f'Expected `admin@admin.com` as email, not `{response.data["email"]}`.')

class UserRetrievePermissionTest(UsersAppTestSetUp):

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
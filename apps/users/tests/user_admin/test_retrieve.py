from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...views import UserAdminViewSet

class UserAdminRetrieveTest(UsersAppTestSetUp):

    def test_user_admin_retrieve(self):
        '''
        Simulate an admin trying to retrieve admin data
        by passing :id as path parameter

        A response should return with specific admin data
        '''
        request = self.factory.get(f'/api/user-admin/{self.admin.uid}/')
        force_authenticate(request, user=self.admin)
        response = UserAdminViewSet.as_view({'get': 'retrieve'})(request, pk=self.admin.uid)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['email'], self.admin.email,
                         f'Expected `{self.admin.email}` as email, not `{response.data["email"]}`.')
        
    def test_user_admin_retrieve_non_admin_user(self):
        '''
        Simulate an admin trying to retrieve admin data
        by passing :id as path parameter
        but that user is not admin (this route is for fetch admin data not normal user)
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/user-admin/{self.user.uid}/')
        force_authenticate(request, user=self.admin)
        response = UserAdminViewSet.as_view({'get': 'retrieve'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         f'Expected http status 404, not {response.status_code}.')
        
class UserAdminRetrievePermissionTest(UsersAppTestSetUp):
    
    def test_user_admin_retrieve_no_permission(self):
        '''
        Simulate a user trying to retrieve admin data
        by passing :id as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/user-admin/{self.admin.uid}/')
        force_authenticate(request, user=self.user)
        response = UserAdminViewSet.as_view({'get': 'retrieve'})(request, pk=self.admin.uid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        
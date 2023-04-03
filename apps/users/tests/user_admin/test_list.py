from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import User
from ...serializers import UserAdminSerializer
from ...views import UserAdminViewSet

class UserAdminListTest(UsersAppTestSetUp):

    def test_user_admin_list_test(self):
        '''
        Simulate an admin trying to fetch all admin in the system

        All admin in the database should show up
        '''
        request = self.factory.get('/api/user-admin/')
        force_authenticate(request, user=self.admin)
        response = UserAdminViewSet.as_view({'get': 'list'})(request)

        admin = User.objects.filter(is_admin=True)
        serializers = UserAdminSerializer(admin, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
                         'Expected to get all admin in database, but the response is not correct.')
        self.assertTrue(len(response.data) == 1,
                        f'Expected 1 admin from list method, not {len(response.data)}.')
    
class UserAdminListPermissionTest(UsersAppTestSetUp):

    def test_user_admin_list_test_no_permission(self):
        '''
        Simulate a user trying to fetch all admin in the system
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get('/api/users/')
        force_authenticate(request, user=self.user)
        response = UserAdminViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
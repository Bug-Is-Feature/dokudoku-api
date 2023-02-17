from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import User
from ...serializers import UserSerializer
from ...views import UserViewSet

class UserListTest(UsersAppTestSetUp):

    def test_user_list_admin(self):
        '''
        Simulate an admin trying to fetch all users in the system

        All users in the database should show up
        '''
        request = self.factory.get('/api/users/')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'get': 'list'})(request)

        users = User.objects.all()
        serializers = UserSerializer(users, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all user in database, but the response is not right.')
        self.assertTrue(len(response.data) == 2,
            f'Expected 2 users from admin view, not {len(response.data)}.')

class UserListPermissionTest(UsersAppTestSetUp):

    def test_user_list_user_no_permission(self):
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
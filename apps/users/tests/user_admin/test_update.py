from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import User
from ...views import UserAdminViewSet

class UserAdminUpdateTest(UsersAppTestSetUp):

    def test_user_admin_update(self):
        '''
        Simulate an admin trying to edit account's admin status

        A response should return with edited account data
        '''
        request = self.factory.put(f'/api/users/{self.user.uid}', {
            "is_admin": True,
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = UserAdminViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(User.objects.get(uid=self.user.uid).is_admin,
                        'Expected updated data has is_admin = True, but the value is not correct.')

class UserAdminUpdatePermissionTest(UsersAppTestSetUp):

    def test_user_admin_update_no_permission(self):
        '''
        Simulate a user trying to edit account's admin status

        An error message should return as response
        '''
        request = self.factory.put(f'/api/users/{self.user.uid}', {
            "is_admin": True,
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserAdminViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertFalse(User.objects.get(uid=self.user.uid).is_admin,
                        'Expected updated data has is_admin = False, but the value is not correct.')

    def test_user_admin_update_forbidden_attribute(self):
        '''
        Simulate an admin trying to edit account's admin status
        but passing attribute other than is_admin
        which is not allowed (this route is for update is_admin only)

        An error message should return as response
        '''
        request = self.factory.put(f'/api/users/{self.user.uid}', {
            "is_admin": True,
            "email": "test_test@admin.com",
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = UserAdminViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertFalse(User.objects.get(uid=self.user.uid).is_admin,
                        'Expected updated data has is_admin = False, but the value is not correct.')
import uuid

from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import User
from ...views import UserAdminViewSet

class UserAdminDestroyTest(UsersAppTestSetUp):

    def test_user_admin_delete(self):
        '''
        Simulate an admin trying to delete other admin account

        A response should return with 204 status
        '''
        alt_admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin2@admin.com',
        )
        request = self.factory.delete(f'/api/user-admin/{alt_admin.uid}/')
        force_authenticate(request, user=self.admin)
        response = UserAdminViewSet.as_view({'delete': 'destroy'})(request, pk=alt_admin.uid)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(User.objects.filter(uid=alt_admin.uid).exists(),
                         f'Expected no admin with uid `{alt_admin.uid}` still exist.')
        
class UserAdminDestroyPermissionTest(UsersAppTestSetUp):

    def test_user_admin_no_permission(self):
        '''
        Simulate a user trying to delete admin account
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/user-admin/{self.admin.uid}/')
        force_authenticate(request, user=self.user)
        response = UserAdminViewSet.as_view({'delete': 'destroy'})(request, pk=self.admin.uid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(User.objects.filter(uid=self.admin.uid).exists(),
                        f'Expected admin with uid `{self.admin.uid}` still exist.')

    def test_user_admin_self_delete(self):
        '''
        Simulate an admin trying to delete their own account
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/user-admin/{self.admin.uid}/')
        force_authenticate(request, user=self.admin)
        response = UserAdminViewSet.as_view({'delete': 'destroy'})(request, pk=self.admin.uid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(User.objects.filter(uid=self.admin.uid).exists(),
                        f'Expected admin with uid `{self.admin.uid}` still exist.')
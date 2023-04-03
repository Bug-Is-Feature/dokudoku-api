import uuid

from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import User
from ...views import UserViewSet

class UserDestroyTest(UsersAppTestSetUp):

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

class UserDestroyPermissionTest(UsersAppTestSetUp):

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
        self.assertTrue(User.objects.filter(uid=self.user.uid).exists(),
            f'Expected user with id: `{self.user.uid}` still exist, but the object got deleted.')
        
    def test_user_delete_user_is_admin(self):
        '''
        Simulate an admin trying to delete other admin
        but deleting admin with /users route is not allowed

        An error message should return as response
        '''
        alt_admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin2@admin.com',
        )
        request = self.factory.delete(f'/api/users/{alt_admin.uid}/')
        force_authenticate(request, user=self.admin)
        response = UserViewSet.as_view({'delete': 'destroy'})(request, pk=alt_admin.uid)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(User.objects.filter(uid=alt_admin.uid).exists(),
                        f'Expected admin with id `{alt_admin.uid}` still exist.')
from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import User
from ...views import UserViewSet

class UserUpdateTest(UsersAppTestSetUp):

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
        self.assertEqual(User.objects.get(uid=self.admin.uid).email, 'edited@edited.com',
            'Expected updated data has email = `edited@edited.com`, but the value is not right.')

class UserUpdatePermissionTest(UsersAppTestSetUp):

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
        self.assertEqual(User.objects.get(uid=self.admin.uid).email, 'admin@admin.com',
            f'Expected no change at user id: {self.admin.uid}, but the object changed.')
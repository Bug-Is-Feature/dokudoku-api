from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import User
from ...views import UserAdminViewSet

class UserIsAdminValidatorTest(UsersAppTestSetUp):

    def test_user_invalid_is_admin_type(self):
        '''
        Simulate an admin trying to edit a user's admin status
        but passing invalid is_admin as attribute (not boolean)

        An error message should return as response
        '''
        request = self.factory.put(f'/api/users/{self.user.uid}/', {
            "is_admin": "not_bool",
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = UserAdminViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(User.objects.get(uid=self.user.uid).is_admin == 'not_bool',
            f'Expected user:{self.user.uid} is_admin has type of `bool`, but the type is wrong.')
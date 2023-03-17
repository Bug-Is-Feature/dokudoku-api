from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import User
from ...views import UserViewSet

class UserCurrentLevelValidatorTest(UsersAppTestSetUp):

    def test_user_validator_invalid_current_lvl_type(self):
        '''
        Simulate a user trying to edit a level
        but passing invalid current_lvl as attribute (not int)
        
        An error message should return as response
        '''
        request = self.factory.put(f'/api/books/{self.user.uid}/', {
            "current_lvl": "abc"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(User.objects.get(uid=self.user.uid).current_lvl == '123',
            f'Expected user:{self.user.uid} current_lvl has type of `int`, but the type is wrong.')

    def test_user_validator_negative_current_lvl(self):
        '''
        Simulate a user trying to edit a level
        but passing invalid current_lvl as attribute (negative int)
        
        An error message should return as response
        '''
        request = self.factory.put(f'/api/books/{self.user.uid}/', {
            "current_lvl": -12
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(User.objects.get(uid=self.user.uid).current_lvl == -12,
            f'Expected user:{self.user.uid} current_lvl has `positive` value, but the value is negative.')
        
class UserCurrentExpValidatorTest(UsersAppTestSetUp):

    def test_user_validator_invalid_current_exp_type(self):
        '''
        Simulate a user trying to edit a level
        but passing invalid current_exp as attribute (not int)
        
        An error message should return as response
        '''
        request = self.factory.put(f'/api/books/{self.user.uid}/', {
            "current_exp": "abc"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(User.objects.get(uid=self.user.uid).current_exp == '123',
            f'Expected user:{self.user.uid} current_exp has type of `int`, but the type is wrong.')

    def test_user_validator_negative_current_exp(self):
        '''
        Simulate a user trying to edit a level
        but passing invalid current_exp as attribute (negative int)
        
        An error message should return as response
        '''
        request = self.factory.put(f'/api/books/{self.user.uid}/', {
            "current_exp": -12
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(User.objects.get(uid=self.user.uid).current_exp == -12,
            f'Expected user:{self.user.uid} current_exp has `positive` value, but the value is negative.')
        
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
        response = UserViewSet.as_view({'put': 'partial_update'})(request, pk=self.user.uid)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(User.objects.get(uid=self.user.uid).is_admin == 'not_bool',
            f'Expected user:{self.user.uid} is_admin has type of `bool`, but the type is wrong.')

from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import SessionsAppTestSetUp
from ...views import SessionViewSet

class SessionQueryParamTest(SessionsAppTestSetUp):

    def test_session_query_param_unknown(self):
        '''
        Simulate a user trying to retrieve session data
        but using unknown parameter in url

        An error message should show up
        '''
        request = self.factory.get('/api/sessions/', {'unknown_params': 'unknown_value'})
        force_authenticate(request, user=self.user)

        with self.assertRaises(FieldError):
            SessionViewSet.as_view({'get': 'list'})(request)

class SessionQueryParamPermissionTest(SessionsAppTestSetUp):

    def test_session_query_param_no_permission(self):
        '''
        Simulate a user trying to retrieve session data
        but passing other user uid as query parameters
        which is not allowed

        An error message should show up
        '''
        request = self.factory.get('/api/sessions/', {'owner': self.admin.uid})
        force_authenticate(request, user=self.user)
        response = SessionViewSet.as_view({'get': 'list'})(request)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
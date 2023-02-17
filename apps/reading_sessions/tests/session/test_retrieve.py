from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import SessionsAppTestSetUp
from ...views import SessionViewSet

class SessionRetrieveTest(SessionsAppTestSetUp):

    def test_session_path_param(self):
        '''
        Simulate a user/admin trying to retrieve session data 
        by passing :id as path parameter

        A response should return with specific session data
        '''
        request = self.factory.get(f'/api/sessions/{self.session_obj.id}/')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'get': 'retrieve'})(request, pk=self.session_obj.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(response.data['duration'] == 300,
            f'Expected `300` as duration, not `{response.data["duration"]}`.')

class SessionRetrievePermissionTest(SessionsAppTestSetUp):

    def test_session_path_param_no_permission(self):
        '''
        Simulate a user trying to retrieve other user's session data 
        by passing :id of that session as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/sessions/{self.session_obj.id}/')
        force_authenticate(request, user=self.user)
        response = SessionViewSet.as_view({'get': 'retrieve'})(request, pk=self.session_obj.id)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')
from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import SessionsAppTestSetUp
from ...models import Session
from ...views import SessionViewSet

class SessionDurationValidatorTest(SessionsAppTestSetUp):

    def test_session_validator_invalid_duration_type(self):
        '''
        Simulate a user trying to create a session
        but passing invalid duration as attribute (not int)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/sessions/', {
            "book_id": self.book_obj.id,
            "duration": 600.50,
            "uid": self.admin.uid
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertTrue(Session.objects.count() == 1,
            'Expected no session created.')

    def test_session_validator_invalid_duration_type(self):
        '''
        Simulate a user trying to create a session
        but passing invalid duration as attribute (negative int)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/sessions/', {
            "book_id": self.book_obj.id,
            "duration": -600,
            "uid": self.admin.uid
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertTrue(Session.objects.count() == 1,
            'Expected no session created.')
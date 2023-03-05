from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import SessionsAppTestSetUp
from ...models import Session
from ...views import SessionViewSet

class SessionUpdateTest(SessionsAppTestSetUp):

    def test_session_update(self):
        '''
        Simulate an admin trying to edit a session

        A response should return with edited session data
        '''
        request = self.factory.put(f'/api/sessions/{self.session_obj.id}/', {
            "duration": 999
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'put': 'partial_update'})(request, pk=self.session_obj.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(Session.objects.get(id=self.session_obj.id).duration == 999,
            'Expected updated data has duration = `999`, but the value is not right.')

class SessionUpdatePermissionTest(SessionsAppTestSetUp):

    def test_session_update_no_permission(self):
        '''
        Simulate a user trying to edit a session
        but editing session is a privilege for admin

        An error message should return as response
        '''
        request = self.factory.put(f'/api/sessions/{self.session_obj.id}/', {
            "duration": 999
        }, format='json')
        force_authenticate(request, user=self.user)
        response = SessionViewSet.as_view({'put': 'partial_update'})(request, pk=self.session_obj.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(Session.objects.get(id=self.session_obj.id).duration == 300,
            f'Expected no change at book id: `{self.session_obj.id}`, but the object changed.')

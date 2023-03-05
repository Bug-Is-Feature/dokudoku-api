from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import SessionsAppTestSetUp
from ...models import Session
from ...views import SessionViewSet

class SessionDestroyTest(SessionsAppTestSetUp):

    def test_session_delete(self):
        '''
        Simulate an admin trying to delete a session

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/sessions/{self.session_obj.id}/')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'delete': 'destroy'})(request, pk=self.session_obj.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(Session.objects.filter(id=self.session_obj.id).exists(),
            f'Expected no session with id `{self.session_obj.id}` still exist.')

class SessionDestroyPermissionTest(SessionsAppTestSetUp):

    def test_session_delete_no_permission(self):
        '''
        Simulate a user trying to delete a session
        but deleting session is a privilege for admin

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/sessions/{self.session_obj.id}/')
        force_authenticate(request, user=self.user)
        response = SessionViewSet.as_view({'delete': 'destroy'})(request, pk=self.session_obj.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')
        self.assertTrue(Session.objects.filter(id=self.session_obj.id).exists(),
            'Expected session still exist, but the object got deleted.')
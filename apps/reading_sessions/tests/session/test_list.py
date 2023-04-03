from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import SessionsAppTestSetUp
from ...models import Session
from ...serializers import SessionSerializer
from ...views import SessionViewSet

class SessionListTest(SessionsAppTestSetUp):

    def test_session_list_admin(self):
        '''
        Simulate an admin trying to fetch all sessions in the system

        All sessions in the database should show up
        '''
        request = self.factory.get('/api/sessions/')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'get': 'list'})(request)

        sessions = Session.objects.all()
        serializers = SessionSerializer(sessions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all session in database, but the response is not right.')
        self.assertTrue(len(response.data) == 1,
            f'Expected 1 session from admin view, not {len(response.data)}.')

    def test_session_list_user(self):
        '''
        Simulate a user trying to fetch all sessions they have in the system

        Every sessions that they own should show up (in this case is 0)
        '''
        request = self.factory.get('/api/sessions/')
        force_authenticate(request, user=self.user)
        response = SessionViewSet.as_view({'get': 'list'})(request)

        sessions = Session.objects.filter(created_by=self.user)
        serializers = SessionSerializer(sessions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all user\'s session in database, but the response is not right.')
        self.assertTrue(len(response.data) == 0,
            f'Expected 0 session from admin view, not {len(response.data)}.')
            
from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import SessionsAppTestSetUp
from ...models import Session
from ...views import SessionViewSet

class SessionCreateTest(SessionsAppTestSetUp):

    def test_session_create(self):
        '''
        Simulate a user trying to create session

        A response should return with newly created session data
        and should be able to access user & book data via response
        '''
        request = self.factory.post('/api/sessions/', {
            "book_id": self.book_obj.id,
            "duration": 600,
            "uid": self.admin.uid
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(Session.objects.filter(book=self.book_obj, duration=600, created_by=self.admin).exists(),
            'Expected session created, but there is no session with data equivalent to input.')
        self.assertEqual(response.data['created_by']['uid'], self.admin.uid,
            f'Expected `{self.admin.uid}` as session owner, not `{response.data["created_by"]["uid"]}`.')
        self.assertEqual(response.data['book']['title'], 'test_book',
            f'Expected `test_book` as title, not `{response.data["book"]["title"]}`.')

class SessionCreatePermissionTest(SessionsAppTestSetUp):
    
    def test_session_create_no_permission(self):
        '''
        Simulate a user trying to create a session
        but passing other user uid as attribute
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.post('/api/sessions/', {
            "book_id": self.book_obj.id,
            "duration": 600,
            "uid": self.admin.uid
        }, format='json')
        force_authenticate(request, user=self.user)
        response = SessionViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertFalse(Session.objects.filter(book=self.book_obj, duration=600, created_by=self.admin).exists(),
            'Expected no session with data equivalent to input exist.')
import uuid

from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.books.models import Book
from apps.users.models import User
from .models import Session
from .views import SessionViewSet

class TestSetUp(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin@admin.com'
        )
        self.user = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user@user.com',
        )

        self.book_obj = Book.objects.create(
            title='test_book',
            subtitle='test_book_sub',
            category='test_book_category',
            thumbnail='test_book_thumbnail',
            description='test_book_desc',
            page_count=284,
            currency_code='THB',
            price=250,
            google_book_id='ed77c79706c3',
        )
        self.session_obj = Session.objects.create(
            book=self.book_obj,
            duration=300,
            created_by=self.admin
        )

class SessionViewSetTest(TestSetUp):

    def test_session_viewset_admin(self):
        '''
        Simulate an admin trying to fetch all sessions in the system

        All sessions in the database should show up
        '''
        request = self.factory.get('/api/sessions/')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 1,
            f'Expected 1 session from admin view, not {len(response.data)}.')

    def test_session_viewset_user(self):
        '''
        Simulate a user trying to fetch all sessions they have in the system

        Every sessions that they own should show up (in this case is 0)
        '''
        request = self.factory.get('/api/sessions/')
        force_authenticate(request, user=self.user)
        response = SessionViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 0,
            f'Expected 0 session from admin view, not {len(response.data)}.')

    def test_session_param_no_permission(self):
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

    def test_session_param_unknown(self):
        '''
        Simulate a user trying to retrieve session data
        but using unknown parameter in url

        An error message should show up
        '''
        request = self.factory.get('/api/sessions/', {'unknown_params': 'unknown_value'})
        force_authenticate(request, user=self.user)

        with self.assertRaises(FieldError):
            SessionViewSet.as_view({'get': 'retrieve'})(request)

    def test_session_create(self):
        '''
        Simulate a user trying to create session

        A response should return with newly created book data
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
        self.assertEqual(response.data['created_by']['uid'], self.admin.uid,
            f'Expected `{self.admin.uid}` as session owner, not `{response.data["created_by"]["uid"]}`.')
        self.assertEqual(response.data['book']['title'], 'test_book',
            f'Expected `test_book` as title, not `{response.data["book"]["title"]}`.')
    
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

    def test_session_update(self):
        '''
        Simulate a admin trying to edit a session

        A response should return with edited session data
        '''
        request = self.factory.put(f'/api/sessions/{self.session_obj.id}/', {
            "duration": 999
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'put': 'partial_update'})(request, pk=self.session_obj.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['duration'], 999,
            f'Expected `999` as duration, not `{response.data["duration"]}`.')

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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_session_delete(self):
        '''
        Simulate a admin trying to delete a session

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/sessions/{self.session_obj.id}/')
        force_authenticate(request, user=self.admin)
        response = SessionViewSet.as_view({'delete': 'destroy'})(request, pk=self.session_obj.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertTrue(len(Session.objects.all()) == 0, 
            f'Expected 0 item remaining after delete, not {len(Book.objects.all())}')

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

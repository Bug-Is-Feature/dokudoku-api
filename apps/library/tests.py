import uuid

from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.users.models import User
from apps.books.models import Book
from .models import Library, LibraryBook
from .views import LibraryViewSet, LibraryBookViewSet

class TestSetUp(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin@admin.com'
        )
        self.user1 = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user1@user.com',
        )
        self.user2 = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user2@user.com'
        )
        self.book_obj1 = Book.objects.create(
            title='test_book_1',
            page_count=156,
            currency_code='THB',
            price=500,
            created_by=self.admin,
        )
        self.book_obj2 = Book.objects.create(
            title='test_book_2',
            page_count=284,
            currency_code='THB',
            price=250,
            google_book_id='ed77c79706c3',
        )
        self.library_obj1 = Library.objects.create(
            created_by=self.admin
        )
        self.library_obj2 = Library.objects.create(
            created_by=self.user1
        )
        self.library_book_obj1 = LibraryBook.objects.create(
            library=self.library_obj1,
            book=self.book_obj1,
            is_completed=False,
        )
        self.library_book_obj2 = LibraryBook.objects.create(
            library=self.library_obj2,
            book=self.book_obj2,
            is_completed=False,
        )

class LibraryViewSetTest(TestSetUp):

    def test_library_viewset_admin(self):
        '''
        Simulate an admin trying to fetch all library in the system

        All library in the database should show up
        '''
        request = self.factory.get('/api/library/')
        force_authenticate(request, self.admin)
        response = LibraryViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 2,
            f'Expected 2 library from admin view, not {len(response.data)}.')

    def test_library_viewset_user(self):
        '''
        Simulate an user trying to fetch their library in the system

        One library which is their own should show up
        '''
        request = self.factory.get('/api/library/')
        force_authenticate(request, user=self.user1)
        response = LibraryViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 1,
            f'Expected only one library from admin view, not {len(response.data)}.')

    def test_library_query_param_unknown(self):
        '''
        Simulate an user trying to retrieve library data
        but using unknown parameter in url

        An error message should show up 
        '''
        request = self.factory.get('/api/library/', {'unknown_params': 'unknown_value'})
        force_authenticate(request, user=self.user1)

        with self.assertRaises(FieldError):
            LibraryViewSet.as_view({'get': 'retrieve'})(request)

    def test_library_path_param(self):
        '''
        Simulate an user/admin trying to retrieve library data
        by passing :id as path parameter

        A response should return with specific library
        '''
        request = self.factory.get(f'/api/library/{self.library_obj1.id}/')
        force_authenticate(request, user=self.admin)
        response = LibraryViewSet.as_view({'get': 'retrieve'})(request, pk=self.library_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['created_by']['uid'], self.admin.uid,
            f'Expected `{self.admin.uid}` as library owner, not `{response.data["created_by"]["uid"]}`.')
        self.assertTrue(len(response.data['books']) == 1,
            f'Expected 1 books in library. not {len(response.data["books"])}.')
    
    def test_library_path_param_no_permission(self):
        '''
        Simulate a user trying to retrieve other user's library data 
        by passing :id of that book as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/library/{self.library_obj1.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryViewSet.as_view({'get': 'retrieve'})(request, pk=self.library_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')

    def test_library_create(self):
        '''
        Simulate an admin trying to create a library

        A response should return with newly created library data
        '''
        request = self.factory.post('/api/library/', {
            "uid": self.user2.uid
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = LibraryViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertEqual(response.data['created_by']['uid'], self.user2.uid,
            f'Expected user `{self.user2.uid}` as library owner, not `{response.data["created_by"]["uid"]}`.')
    
    def test_library_create_no_permission(self):
        '''
        Simulate an user trying to create a library
        with /api/library/ route
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.post('/api/library/', {
            "uid": self.user1.uid
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_library_update(self):
        '''
        Simulate an admin trying to edit a library data

        A response should return with edited library data
        '''
        request = self.factory.put(f'/api/library/{self.library_obj2.id}/', {
            "uid": self.user2.uid
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = LibraryViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['created_by']['uid'], self.user2.uid,
            f'Expected `{self.user2.uid}` as library owner, not {response.data["created_by"]["uid"]}.')

    def test_library_update_no_permission(self):
        '''
        Simulate an user trying to edit a library data
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.put(f'/api/library/{self.library_obj2.id}/', {
            "uid": self.user2.uid
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_library_delete(self):
        '''
        Simulate an admin trying to delete a library

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/library/{self.library_obj2.id}/')
        force_authenticate(request, user=self.admin)
        response = LibraryViewSet.as_view({'delete': 'destroy'})(request, pk=self.library_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(Library.objects.filter(id=self.library_obj2.id).exists(),
            f'Expected no library with id `{self.library_obj2.id}` exist.')

    def test_library_delete_no_permission(self):
        '''
        Simulate a user trying to delete a library
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/library/{self.library_obj2.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryViewSet.as_view({'delete': 'destroy'})(request, pk=self.library_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

class LibraryBookViewSetTest(TestSetUp):
    
    def test_library_book_viewset_admin(self):
        '''
        Simulate an admin trying to fetch all book in user library

        All book from every library is the database should show up
        '''
        request = self.factory.get('/api/library-books/')
        force_authenticate(request, user=self.admin)
        response = LibraryBookViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 2,
            f'Expected 2 books from admin view. not {len(response.data)}.')

    def test_library_book_viewset_user(self):
        '''
        Simulate an user trying to fetch every book in their library

        Every books in their library should show up (in this case is 0)
        '''
        request = self.factory.get('/api/library-books/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 1,
            f'Expected 1 book from user view, not {len(response.data)}.')

    def test_book_query_param_unknown(self):
        '''
        Simulate an user trying to retrieve book in library
        but using unknown parameter in url

        An error message should show up
        '''
        request = self.factory.get('/api/library-books/', {'unknown_params': 'unknown_value'})
        force_authenticate(request, user=self.user1)

        with self.assertRaises(FieldError):
            LibraryBookViewSet.as_view({'get': 'retrieve'})(request)

    def test_library_book_path_param(self):
        '''
        Simulate an user/admin trying to retrieve book in library 
        by passing :id as path parameter

        A response should return with specific book data
        '''
        request = self.factory.get(f'/api/library-books/{self.library_book_obj1.id}/')
        force_authenticate(request, user=self.admin)
        response = LibraryBookViewSet.as_view({'get': 'retrieve'})(request, pk=self.library_book_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['book']['id'], self.book_obj1.id,
            f'Expected `{self.book_obj1.id}` as book id, not `{response.data["book"]["id"]}`.')

    def test_library_book_path_param_no_permission(self):
        '''
        Simulate an user trying to retrieve book in other user's library 
        by passing :id of that book as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/library-books/{self.library_book_obj1.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'get': 'retrieve'})(request, pk=self.library_book_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')

    def test_library_book_auto_create_user_library(self):
        '''
        Simulate an user trying to add a book into library
        but a library with user as owner is not exist

        Library of the user should created automatically
        '''
        book = self.book_obj2.__dict__
        book.pop('_state')
        request = self.factory.post('/api/library-books/', {
            "book_data": book,
        },format='json')
        force_authenticate(request, user=self.user2)
        response = LibraryBookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(Library.objects.filter(created_by=self.user2).exists(),
            f'Expected library of user `{self.user2.uid}` created automatically, but the library is not found.')
    
    def test_library_book_auto_create_book(self):
        '''
        Simulate an user trying to add a book into library

        Custom book should created automatically if not exist in database
        '''
        request = self.factory.post('/api/library-books/', {
            "book_data": {
                "title": "test_library_book_create",
                "page_count": 111,
                "currency_code": "THB",
                "price": 123,
                "created_by": self.user1.uid,
            },
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(Book.objects.filter(title='test_library_book_create').exists(),
            f'Expected book with title `test_library_book_create` created automatically, but the book is not found.')

    def test_library_book_create_no_permission(self):
        '''
        Simulate an user trying to add other user's custom book into library
        which is not allowed

        An error message should return as response
        '''
        book = self.book_obj1.__dict__
        book.pop('_state')
        book['created_by'] = book.pop('created_by_id')
        request = self.factory.post('/api/library-books/', {
            "book_data": book,
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_library_book_update(self):
        '''
        Simulate an user trying to edit a book reading status

        A response should return with edited library_book data
        '''
        request = self.factory.put(f'/api/library-books/{self.library_book_obj1.id}/', {
            "is_completed": True
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = LibraryBookViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(response.data['is_completed'],
            f'Expected is_completed = true, not `{response.data["is_completed"]}`.')

    def test_library_book_update_no_permission(self):
        '''
        Simulate an user trying to edit a book in other user library
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.put(f'/api/library-books/{self.library_book_obj1.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')

    def test_library_book_update_forbidden_attribute(self):
        '''
        Simulate an user trying to edit a book reading status
        but edit attribute that is not is_completed

        An error message should return as response
        '''
        book = self.book_obj1.__dict__
        book.pop('_state')
        request = self.factory.put(f'/api/library-books/{self.library_book_obj2.id}/', {
            "book": book
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_book_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 200, not {response.status_code}.')

    def test_library_book_delete(self):
        '''
        Simulate an user trying to delete a book in library

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/library-books/{self.library_book_obj2.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'delete': 'destroy'})(request, pk=self.library_book_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(LibraryBook.objects.filter(id=self.library_book_obj2.id).exists(),
            f'Expected no library_book with id `{self.library_book_obj2.id}` still exist.')

    def test_library_book_delete_no_permission(self):
        '''
        Simulate an user trying to delete a book from other user library
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/library-books/{self.library_book_obj1.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'delete': 'destroy'})(request, pk=self.library_book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')

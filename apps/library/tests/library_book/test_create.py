from rest_framework import status
from rest_framework.test import force_authenticate

from apps.books.models import Author, Book
from ..test_setup import LibraryAppTestSetUp
from ...models import Library, LibraryBook
from ...views import LibraryBookViewSet

class LibraryBookCreateTest(LibraryAppTestSetUp):

    def test_library_book_create(self):
        '''
        Simulate a user trying to add a book into library

        A response should return with newly created library_book
        '''
        book = Book.objects.create(
            title='test_book_3',
            page_count=234,
            currency_code='THB',
            price=750,
            created_by=self.user1,
        ).__dict__
        book.pop('_state')
        request = self.factory.post('/api/library-books', {
            "book_data": book,
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(LibraryBook.objects.count() == 3,
            f'Expected total 3 library_book items after created, not {LibraryBook.objects.count()}.')

    def test_library_book_auto_create_library(self):
        '''
        Simulate a user trying to add a book into library
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
        Simulate a user trying to add a book into library

        Custom book should created automatically if not exist in database
        '''
        request = self.factory.post('/api/library-books/', {
            "book_data": {
                "title": "test_library_book_create",
                "page_count": 111,
                "currency_code": "THB",
                "price": 123,
                "created_by": self.user1.uid,
                "authors": [
                    {
                        "name": " test_library_book_author "
                    }
                ]
            },
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(Library.objects.get(created_by=self.user1).is_changed,
            'Expected library is_changed = `True`, but the value is not right.')
        created_book = Book.objects.filter(title='test_library_book_create')
        self.assertTrue(created_book.exists(),
            'Expected book with title `test_library_book_create` created automatically, but the book is not found.')
        self.assertTrue(Author.objects.filter(name='test_library_book_author').exists(),
            'Expected author with name `test_library_book_author` created, but the author is not found.')
        self.assertEqual(Author.objects.get(name='test_library_book_author').book, *created_book,
            'Expected author `test_library_book_author` to have book = `test_library_book_create`, but the value is not right.')

class LibraryBookCreatePermissionTest(LibraryAppTestSetUp):

    def test_library_book_create_no_permission(self):
        '''
        Simulate a user trying to add other user's custom book into library
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
        self.assertFalse(Library.objects.get(created_by=self.user1).is_changed,
            'Expected library is_changed = `False`, but the value is not right.')
        self.assertFalse(LibraryBook.objects.count() > 2,
            f'Expected only 2 library_book exist, not {LibraryBook.objects.count()}.')
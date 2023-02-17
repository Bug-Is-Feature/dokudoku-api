from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...models import Book
from ...views import BookViewSet

class BookCreateTest(BooksAppTestSetUp):

    def test_book_create(self):
        '''
        Simulate a user trying to create a book

        A response should return with newly created book data
        and should be able to access user & authors data via response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_book_title",
            "subtitle": "test_book_subtitle",
            "category": "test_book_category",
            "thumbnail": "test_book_thumbnail",
            "description": "test_book_desc",
            "page_count": 134,
            "currency_code": "THB",
            "price": 100,
            "uid": self.user.uid,
            "authors": [
                {
                    "name": "test_book_author"
                }
            ]
        }, format='json')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(Book.objects.filter(title='test_book_title').exists(),
            'Expected book with title `test_book_title` exist, but the book is not found.')
        self.assertEqual(response.data['title'], 'test_book_title',
            f'Expected `test_book_title` as book title, not `{response.data["title"]}`.')
        self.assertEqual(response.data['created_by']['uid'], self.user.uid,
            f'Expected `{self.user.uid}` as book owner, not `{response.data["created_by"]["uid"]}`.')
        self.assertEqual(response.data['authors'][0]['name'], 'test_book_author',
            f'Expected `test_book_author` as author name, not `{response.data["authors"][0]["name"]}`.')

    def test_book_create_unique_google_book_id(self):
        '''
        Simulate a user trying to create a google book
        but the book is already exist in database

        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_book_2",
            "page_count": 284,
            "currency_code": "THB",
            "price": 250,
            "google_book_id": "ed77c79706c3"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertTrue(Book.objects.filter(google_book_id='ed77c79706c3').count() == 1,
            'Expected only one book with google_book_id: `ed77c79706c3`.')

    def test_book_create_forbidden_action(self):
        '''
        Simulate a user trying to create a book
        but passing both 2 attributes (uid, google_book_id) 
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_book_title",
            "subtitle": "test_book_subtitle",
            "category": "test_book_category",
            "thumbnail": "test_book_thumbnail",
            "description": "test_book_desc",
            "page_count": 134,
            "currency_code": "THB",
            "price": 100,
            "uid": self.user.uid,
            "google_book_id": "ed77c79706c3",
            "authors": [
                {
                    "name": "test_book_author"
                }
            ]
        }, format='json')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(title='test_book_title').exists(),
            'Expected no book with title `test_book_title`, but the book created with out permission.')

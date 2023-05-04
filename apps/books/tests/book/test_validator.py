from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...models import Book
from ...views import BookViewSet

class BookPageCountValidatorTest(BooksAppTestSetUp):

    def test_book_validator_invalid_page_count_type(self):
        '''
        Simulate an admin trying to create a book
        but passing invalid page_count as attribute (not int)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_invalid_type_page_count",
            "page_count": 1.32,
            "price": 100.0,
            "google_book_id": "123456789012"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(title='test_invalid_page_count').exists(),
            'Expected no book with title `test_invalid_page_count`, but the book is created.')

    def test_book_validator_negative_page_count(self):
        '''
        Simulate an admin trying to create a book
        but passing invalid page_count as attribute (negative int)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_negative_page_count",
            "page_count": -1,
            "price": 100.0,
            "google_book_id": "123456789012"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(title='test_invalid_page_count').exists(),
            'Expected no book with title `test_negative_page_count`, but the book is created.')

class BookCurrencyCodeValidatorTest(BooksAppTestSetUp):

    def test_book_validator_invalid_iso4217(self):
        '''
        Simulate an admin trying to create a book
        but passing invalid currency_code as attribute (not ISO 4217)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_invalid_currency_code",
            "page_count": 10,
            "currency_code": "XXX",
            "price": 100.0,
            "google_book_id": "123456789012"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(title='test_invalid_currency_code').exists(),
            'Expected no book with title `test_invalid_currency_code`, but the book is created.')

class BookPriceValidatorTest(BooksAppTestSetUp):

    def test_book_validator_invalid_price_type(self):
        '''
        Simulate an admin trying to create a book
        but passing invalid price as attribute (not int)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_negative_price",
            "page_count": 100,
            "price": "100",
            "google_book_id": "123456789012"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(title='test_negative_price').exists(),
            'Expected no book with title `test_negative_price`, but the book is created.')

    def test_book_validator_negative_price(self):
        '''
        Simulate an admin trying to create a book
        but passing invalid price as attribute (negative int)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_negative_price",
            "page_count": 100,
            "price": -100.0,
            "google_book_id": "123456789012"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(title='test_negative_price').exists(),
            'Expected no book with title `test_negative_price`, but the book is created.')

class BookGoogleBookIdValidatorTest(BooksAppTestSetUp):

    def test_book_validator_google_book_id(self):
        '''
        Simulate an admin trying to create a book
        but passing invalid google_book_id as attribute (string length != 12)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_google_book_id",
            "page_count": 100,
            "price": 100.0,
            "google_book_id": "1234567890"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(title='test_google_book_id').exists(),
            'Expected no book with title `test_google_book_id`, but the book is created.')

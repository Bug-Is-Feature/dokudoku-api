from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...models import Book
from ...views import BookViewSet

class BookDeleteTest(BooksAppTestSetUp):

    def test_book_delete(self):
        '''
        Simulate a user/admin trying to delete a book

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/books/{self.book_obj1.id}/')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'delete': 'destroy'})(request, pk=self.book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(id=self.book_obj1.id).exists(),
            f'Expected no book with id `{self.book_obj1.id}` still exist.')

class BookDeletePermissionTest(BooksAppTestSetUp):

    def test_book_delete_no_permission(self):
        '''
        Simulate a user trying to delete a book 
        which is not allowed (user need to user /library-books path)
        
        An error message should return as response
        '''
        book = Book.objects.create(
            title='test_book_permission',
            page_count=284,
            currency_code='THB',
            price=250,
            created_by=self.user
        )
        request = self.factory.delete(f'/api/books/{book.id}/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'delete': 'destroy'})(request, pk=book.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(Book.objects.filter(id=self.book_obj1.id).exists(),
            f'Expected book with id `{self.book_obj1.id}` still exist, but the book got deleted with out permission.')
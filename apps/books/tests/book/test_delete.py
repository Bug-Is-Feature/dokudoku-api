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
        but don't have a permission (not the owner of the book)
        
        An error message should return as response
        '''
        request = self.factory.delete(f'/api/books/{self.book_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'delete': 'destroy'})(request, pk=self.book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')
        self.assertTrue(Book.objects.filter(id=self.book_obj1.id).exists(),
            f'Expected book with id `{self.book_obj1.id}` still exist, but the book got deleted with out permission.')
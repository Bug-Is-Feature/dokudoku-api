from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...views import BookViewSet

class BookRetrieveTest(BooksAppTestSetUp):

    def test_book_retrieve(self):
        '''
        Simulate a user/admin trying to retrieve book data 
        by passing :id as path parameter

        A response should return with specific book data
        '''
        request = self.factory.get(f'/api/books/{self.book_obj1.id}/')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'get': 'retrieve'})(request, pk=self.book_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['title'], 'test_book_1',
            f'Expected `test_book_1` as title, not `{response.data["title"]}`.')

class BookRetrievePermissionTest (BooksAppTestSetUp):

    def test_book_retrieve_no_permission(self):
        '''
        Simulate a user trying to retrieve other user's book data 
        by passing :id of that book as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/books/{self.book_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'get': 'retrieve'})(request, pk=self.book_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')

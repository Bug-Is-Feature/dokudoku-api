from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...views import AuthorViewSet

class AuthorRetrieveTest(BooksAppTestSetUp):

    def test_author_retrieve(self):
        '''
        Simulate a user/admin trying to retrieve author data 
        by passing :id as path parameter

        A response should return with specific author data
        '''
        request = self.factory.get(f'/api/authors/{self.author_obj1.id}/')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'get': 'retrieve'})(request, pk=self.author_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['name'], 'test_book_1_author',
            f'Expected `test_book_1_author` as name, not `{response.data["name"]}`.')

class AuthorRetrievePermissionTest(BooksAppTestSetUp):

    def test_author_retrieve_no_permission(self):
        '''
        Simulate a user trying to retrieve other user book's author 
        by passing :id of that author as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/authors/{self.author_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'get': 'retrieve'})(request, pk=self.author_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
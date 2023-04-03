from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...views import LibraryBookViewSet

class LibraryBookRetrieveTest(LibraryAppTestSetUp):

    def test_library_book_retrieve(self):
        '''
        Simulate a user/admin trying to retrieve book in library 
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

class LibraryBookRetrievePermissionTest(LibraryAppTestSetUp):

    def test_library_book_retrieve_no_permission(self):
        '''
        Simulate a user trying to retrieve book in other user's library 
        by passing :id of that book as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/library-books/{self.library_book_obj1.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'get': 'retrieve'})(request, pk=self.library_book_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')
from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...views import LibraryViewSet

class LibraryRetrieveTest(LibraryAppTestSetUp):

    def test_library_retrieve(self):
        '''
        Simulate a user/admin trying to retrieve library data
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

class LibraryRetrievePermissionTest(LibraryAppTestSetUp):

    def test_library_retrieve_no_permission(self):
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
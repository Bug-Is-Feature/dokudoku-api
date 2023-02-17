from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...models import Library
from ...views import LibraryViewSet

class LibraryCreateTest(LibraryAppTestSetUp):

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
        self.assertTrue(Library.objects.filter(created_by=self.user2.uid).exists(),
            f'Expected library of user `{self.user2.uid}` exist, but the library is not found.')

class LibraryCreatePermissionTest(LibraryAppTestSetUp):
    
    def test_library_create_no_permission(self):
        '''
        Simulate a user trying to create a library
        with /api/library/ route
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.post('/api/library/', {
            "uid": self.user2.uid
        }, format='json')
        force_authenticate(request, user=self.user2)
        response = LibraryViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertFalse(Library.objects.filter(created_by=self.user2).exists(),
            f'Expected no library of user `{self.user2.uid}`, but the library created with out permission.')
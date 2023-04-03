from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...models import Library
from ...views import LibraryViewSet

class LibraryDestroyTest(LibraryAppTestSetUp):

    def test_library_delete(self):
        '''
        Simulate an admin trying to delete a library

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/library/{self.library_obj2.id}/')
        force_authenticate(request, user=self.admin)
        response = LibraryViewSet.as_view({'delete': 'destroy'})(request, pk=self.library_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(Library.objects.filter(id=self.library_obj2.id).exists(),
            f'Expected no library with id `{self.library_obj2.id}` exist.')

class LibraryDestroyPermissionTest(LibraryAppTestSetUp):

    def test_library_delete_no_permission(self):
        '''
        Simulate a user trying to delete a library
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/library/{self.library_obj2.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryViewSet.as_view({'delete': 'destroy'})(request, pk=self.library_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(Library.objects.filter(id=self.library_obj2.id).exists(),
            f'Expected library still exist, but the object got deleted.')
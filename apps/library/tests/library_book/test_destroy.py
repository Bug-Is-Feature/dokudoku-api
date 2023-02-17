from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...models import LibraryBook
from ...views import LibraryBookViewSet

class LibraryBookDestroyTest(LibraryAppTestSetUp):
    
    def test_library_book_delete(self):
        '''
        Simulate a user trying to delete a book in library

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/library-books/{self.library_book_obj2.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'delete': 'destroy'})(request, pk=self.library_book_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(LibraryBook.objects.filter(id=self.library_book_obj2.id).exists(),
            f'Expected no library_book with id `{self.library_book_obj2.id}` still exist.')

class LibraryBookDestroyPermissionTest(LibraryAppTestSetUp):

    def test_library_book_delete_no_permission(self):
        '''
        Simulate a user trying to delete a book from other user library
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/library-books/{self.library_book_obj1.id}/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'delete': 'destroy'})(request, pk=self.library_book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')
        self.assertTrue(LibraryBook.objects.filter(id=self.library_book_obj1.id).exists(),
            'Expected library_book still exist, but the object got deleted.')
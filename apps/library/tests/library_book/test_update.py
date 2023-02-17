from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...models import LibraryBook
from ...views import LibraryBookViewSet

class LibraryBookUpdateTest(LibraryAppTestSetUp):

    def test_library_book_update(self):
        '''
        Simulate a user trying to edit a book reading status

        A response should return with edited library_book data
        '''
        request = self.factory.put(f'/api/library-books/{self.library_book_obj1.id}/', {
            "is_completed": True
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = LibraryBookViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(LibraryBook.objects.get(id=self.library_book_obj1.id).is_completed,
            f'Expected updated data has is_completed = `{True}`, but the value is not right.')

    def test_library_book_update_forbidden_attribute(self):
        '''
        Simulate a user trying to edit a book reading status
        but edit attribute that is not is_completed

        An error message should return as response
        '''
        book = self.book_obj1.__dict__
        book.pop('_state')
        request = self.factory.put(f'/api/library-books/{self.library_book_obj2.id}/', {
            "book": book
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_book_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertEqual(LibraryBook.objects.get(id=self.library_book_obj2.id).book, self.book_obj2,
            'Expected no change when update with forbidden attribute, but the value is changed.')

class LibraryBookUpdatePermissionTest(LibraryAppTestSetUp):

    def test_library_book_update_no_permission(self):
        '''
        Simulate a user trying to edit a book in other user library
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.put(f'/api/library-books/{self.library_book_obj1.id}/', {
            "is_completed": True
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')
        self.assertFalse(LibraryBook.objects.get(id=self.library_book_obj1.id).is_completed,
            f'Expected no change on library_book with id `{self.library_book_obj1.id}`, but the value is changed.')

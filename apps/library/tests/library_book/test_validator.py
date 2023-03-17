from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...models import LibraryBook
from ...views import LibraryBookViewSet

class LibraryBookIsCompletedValidatorTest(LibraryAppTestSetUp):

    def test_library_book_invalid_is_completed_type(self):
        '''
        Simulate a user trying to add a book into library
        but passing invalid is_completed as attribute (not boolean)

        An error message should return as response
        '''
        book = self.book_obj2.__dict__
        book.pop('_state')
        request = self.factory.post('/api/library-books', {
            "book_data": book,
            "is_completed": "not_bool",
        }, format='json')
        force_authenticate(request, user=self.user2)
        response = LibraryBookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertTrue(LibraryBook.objects.count() == 2,
            f'Expected total 2 library_book items after created, not {LibraryBook.objects.count()}.')
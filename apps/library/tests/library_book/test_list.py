from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...models import LibraryBook
from ...serializers import LibraryBookSerializer
from ...views import LibraryBookViewSet

class LibraryBookListTest(LibraryAppTestSetUp):
    
    def test_library_book_list_admin_view(self):
        '''
        Simulate an admin trying to fetch all book in user library

        All book from every library is the database should show up
        '''
        request = self.factory.get('/api/library-books/')
        force_authenticate(request, user=self.admin)
        response = LibraryBookViewSet.as_view({'get': 'list'})(request)

        library_books = LibraryBook.objects.all()
        serializers = LibraryBookSerializer(library_books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all library_book in the database, but the response is not right.')
        self.assertTrue(len(response.data) == 2,
            f'Expected 2 books from admin view. not {len(response.data)}.')

    def test_library_book_list_user_view(self):
        '''
        Simulate a user trying to fetch every book in their library

        Every books in their library should show up (in this case is 0)
        '''
        request = self.factory.get('/api/library-books/')
        force_authenticate(request, user=self.user1)
        response = LibraryBookViewSet.as_view({'get': 'list'})(request)

        library_books = LibraryBook.objects.filter(library=self.library_obj2.id)
        serializers = LibraryBookSerializer(library_books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all books in user\'s library, but the response is not right.')
        self.assertTrue(len(response.data) == 1,
            f'Expected 1 book from user view, not {len(response.data)}.')

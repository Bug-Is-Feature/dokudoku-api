from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...models import Book
from ...serializers import BookSerializer
from ...views import BookViewSet

class BookListTest(BooksAppTestSetUp):

    def test_book_list_admin_view(self):
        '''
        Simulate an admin trying to fetch all books in the system

        All books in the database should show up
        '''
        request = self.factory.get('/api/books/')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'get': 'list'})(request)

        books = Book.objects.all()
        serializers = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all book in the database, but the response is not right.')
        self.assertTrue(len(response.data) == 2,
            f'Expected 2 books from admin view, not {len(response.data)}.')

    def test_book_list_user_view(self):
        '''
        Simulate a user trying to fetch all books they have in the system

        Every books that they own should show up (in this case is 0)
        '''
        request = self.factory.get('/api/books/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'get': 'list'})(request)

        books = Book.objects.filter(created_by=self.user)
        serializers = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all user custom book, but the response is not right.')
        self.assertTrue(len(response.data) == 0,
            f'Expected 0 book from user view, not {len(response.data)}.')

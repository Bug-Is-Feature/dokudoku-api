from rest_framework import status
from rest_framework.test import force_authenticate

from apps.library.models import Library
from ..test_setup import BooksAppTestSetUp
from ...models import Book
from ...views import BookViewSet

class BookUpdateTest(BooksAppTestSetUp):

    def test_book_update(self):
        '''
        Simulate a user/admin trying to edit a book

        A response should return with edited book data
        '''
        request = self.factory.put(f'/api/books/{self.book_obj1.id}/', {
            "subtitle": "edited_subtitle"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'put': 'partial_update'})(request, pk=self.book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(Book.objects.get(id=self.book_obj1.id).subtitle, 'edited_subtitle',
            f'Expected updated data has subtitle = `edited_subtitle`, but the value is not right.')
        self.assertTrue(Library.objects.get(created_by=self.admin).is_changed,
            'Expected library is_changed = `True`, but the value is not right.')

class BookUpdatePermissionTest(BooksAppTestSetUp):

    def test_book_update_no_permission(self):
        '''
        Simulate a user trying to edit a book
        but don't have a permission (not the owner of the book)
        
        An error message should return as response
        '''
        request = self.factory.put(f'/api/books/{self.book_obj1.id}/', {
            "subtitle": "edited_subtitle"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'put': 'partial_update'})(request, pk=self.book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')
        self.assertEqual(Book.objects.get(id=self.book_obj1.id).subtitle, 'test_book_1_sub',
            f'Expected no change at book id: `{self.book_obj1.id}`, but the object changed.')
        self.assertFalse(Library.objects.get(created_by=self.user).is_changed,
            'Expected library is_changed = `False`, but the value is not right.')

from rest_framework import status
from rest_framework.test import force_authenticate

from apps.library.models import Library
from ..test_setup import BooksAppTestSetUp
from ...models import Author
from ...views import AuthorViewSet

class AuthorUpdateTest(BooksAppTestSetUp):

    def test_author_update(self):
        '''
        Simulate a user/admin trying to edit a book's author

        A response should return with edited author data
        '''
        request = self.factory.put(f'/api/authors/{self.author_obj1.id}/', {
            "name": "test_book_1_author_edited"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'put': 'partial_update'})(request, pk=self.author_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(Author.objects.get(id=self.author_obj1.id).name, 'test_book_1_author_edited',
            'Expected updated data has name = `test_book_1_author_edited`, but the value is not right.')
        self.assertTrue(Library.objects.get(created_by=self.admin).is_changed,
            'Expected library is_changed = `True`, but the value is not right.')

class AuthorUpdatePermissionTest(BooksAppTestSetUp):

    def test_author_update_no_permission(self):
        '''
        Simulate a user/admin trying to edit a book's author
        but don't have a permission (not the owner of the book)

        An error message should return as response
        '''
        request = self.factory.put(f'/api/authors/{self.author_obj2.id}/', {
            "name": "test_book_2_author_1_edited"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'put': 'partial_update'})(request, pk=self.author_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertEqual(Author.objects.get(id=self.author_obj2.id).name, 'test_book_2_author_1',
            f'Expected no change at author id: {self.author_obj2.id}, but the object changed.')
        self.assertFalse(Library.objects.get(created_by=self.user).is_changed,
            'Expected library is_changed = `False`, but the value is not right.')
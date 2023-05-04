from rest_framework import status
from rest_framework.test import force_authenticate

from apps.library.models import Library
from ..test_setup import BooksAppTestSetUp
from ...models import Author
from ...views import AuthorViewSet

class AuthorDeleteTest(BooksAppTestSetUp):

    def test_author_delete(self):
        '''
        Simulate a user/admin trying to delete a book's author

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/authors/{self.author_obj3.id}/')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'delete': 'destroy'})(request, pk=self.author_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(Author.objects.filter(id=self.author_obj3.id).exists(),
            f'Expected no author with id `{self.author_obj3.id}` still exist.')
        self.assertTrue(Library.objects.get(created_by=self.admin).is_changed,
            'Expected library is_changed = `True`, but the value is not right.')

class AuthorDeletePermissionTest(BooksAppTestSetUp):

    def test_author_delete_no_permission(self):
        '''
        Simulate a user trying to delete a book 's author
        but don't have a permission (not the owner of the book)
        
        An error message should return as response
        '''
        request = self.factory.delete(f'/api/authors/{self.author_obj3.id}/')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'delete': 'destroy'})(request, pk=self.author_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(Author.objects.filter(id=self.author_obj3.id).exists(),
            f'Expected author with id `{self.author_obj3.id}` still exist, but the object got deleted.')
        self.assertFalse(Library.objects.get(created_by=self.user).is_changed,
            'Expected library is_changed = `False`, but the value is not right.')
from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...models import Author
from ...views import AuthorViewSet

class AuthorCreateTest(BooksAppTestSetUp):

    def test_author_create(self):
        '''
        Simulate a user/admin trying to create a book's author

        A response should return with newly created author data
        '''
        request = self.factory.post('/api/authors/', {
            "name": "test_create_author",
            "book_id": self.book_obj1.id
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(Author.objects.filter(name='test_create_author').exists(),
            'Expected `test_create_author` existed, but the author is not found.')

class AuthorCreatePermissionTest(BooksAppTestSetUp):

    def test_author_create_no_permission(self):
        '''
        Simulate a user/admin trying to create a book's author
        but don't have a permission (not the owner of the book)

        An error message should return as response
        '''
        request = self.factory.post('/api/authors/', {
            "name": "test_create_author",
            "book_id": self.book_obj2.id
        }, format='json')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'post': 'create'})(request)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertFalse(Author.objects.filter(name='test_create_author').exists(),
            'Expected no author with name `test_create_author`, but the author created with out permission.')

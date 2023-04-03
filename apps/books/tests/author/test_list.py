from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...models import Author
from ...serializers import AuthorSerializer
from ...views import AuthorViewSet

class AuthorListTest(BooksAppTestSetUp):

    def test_author_list_admin_view(self):
        '''
        Simulate an admin trying to fetch all authors in the system

        All authors in the database should show up
        '''
        request = self.factory.get('/api/authors/')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'get': 'list'})(request)

        authors = Author.objects.all()
        serializers = AuthorSerializer(authors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all authors in the database, but the response is not right.')
        self.assertTrue(len(response.data) == 3,
            f'Expected 3 authors from admin view, not {len(response.data)}.')

class AuthorListPermissionTest(BooksAppTestSetUp):

    def test_author_list_no_permission(self):
        '''
        Simulate a user trying to fetch all authors in the system
        but fetching all authors is a privilege for admin

        An error message should return as response
        '''
        request = self.factory.get('/api/authors/')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

from django.core.exceptions import FieldError
from rest_framework.test import force_authenticate

from ..test_setup import BooksAppTestSetUp
from ...views import BookViewSet

class BookQueryParamTest(BooksAppTestSetUp):

    def test_book_query_param_forbidden_action(self):
        '''
        Simulate a user trying to retrieve book data
        but passing both 2 query parameters (ggbookid, owner)
        which is not allowed

        An error message should show up
        '''
        request = self.factory.get('/api/books/', 
            {'ggbookid': 'ed77c79706c3', 'owner': self.admin.uid})
        force_authenticate(request, user=self.user)

        with self.assertRaises(FieldError):
            BookViewSet.as_view({'get': 'retrieve'})(request)

    def test_book_query_param_unknown(self):
        '''
        Simulate a user trying to retrieve book data
        but using unknown parameter in url

        An error message should show up
        '''
        request = self.factory.get('/api/books/', {'unknown_params': 'unknown_value'})
        force_authenticate(request, user=self.user)

        with self.assertRaises(FieldError):
            BookViewSet.as_view({'get': 'retrieve'})(request)
from django.core.exceptions import FieldError
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...views import LibraryBookViewSet

class LibraryBookQueryParamTest(LibraryAppTestSetUp):

    def test_book_query_param_unknown(self):
        '''
        Simulate a user trying to retrieve book in library
        but using unknown parameter in url

        An error message should show up
        '''
        request = self.factory.get('/api/library-books/', {'unknown_params': 'unknown_value'})
        force_authenticate(request, user=self.user1)

        with self.assertRaises(FieldError):
            LibraryBookViewSet.as_view({'get': 'retrieve'})(request)
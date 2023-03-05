from django.core.exceptions import FieldError
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...views import LibraryViewSet

class LibraryQueryParamTest(LibraryAppTestSetUp):

    def test_library_query_param_unknown(self):
        '''
        Simulate a user trying to retrieve library data
        but using unknown parameter in url

        An error message should show up 
        '''
        request = self.factory.get('/api/library/', {'unknown_params': 'unknown_value'})
        force_authenticate(request, user=self.user1)

        with self.assertRaises(FieldError):
            LibraryViewSet.as_view({'get': 'retrieve'})(request)
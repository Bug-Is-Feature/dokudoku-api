from rest_framework import status
from rest_framework.test import force_authenticate

from apps.library.models import Library
from ..test_setup import RecommenderAppTestSetUp
from ...views import RecommenderViewSet

class RecommenderListTest(RecommenderAppTestSetUp):

    def test_recommender_list(self):
        '''
        Simulate a user trying to get book recommendation

        Recommended book should return as response
        '''
        request = self.factory.get(f'/api/recommendation/')
        force_authenticate(request, user=self.user1)
        response = RecommenderViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 1,
            f'Expected only one book as recommend result, not {len(response.data)}.')
        
    def test_recommender_list_no_library(self):
        '''
        Simulate a user trying to get book recommendation
        but user not have library

        A library should create automatically,
        and error message should return as response because user have no book.
        '''
        request = self.factory.get(f'/api/recommendation/')
        force_authenticate(request, user=self.user2)
        response = RecommenderViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')
        self.assertTrue(Library.objects.filter(created_by=self.user2).exists(),
            'Expected library to create automatically, but the library is not found.')


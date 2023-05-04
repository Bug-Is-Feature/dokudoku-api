import os

from rest_framework import status
from rest_framework.test import force_authenticate

from apps.library.models import Library, LibraryBook
from ..test_setup import RecommenderAppTestSetUp
from ...exceptions import InsufficientBookError
from ...recommender import BookRecommender
from ...views import RecommenderViewSet

class CreateRecommenderTest(RecommenderAppTestSetUp):

    def test_create_recommender(self):
        '''
        Simulate a system trying to create user's book recommendation

        A result file should be created and saved correctly
        '''
        recommender = BookRecommender()
        recommender.create_recommend_result(user=self.user1)

        self.assertTrue(os.path.exists(self.path + f'/{self.user1.uid}.txt'),
            'Expected recommend result exist, but the file is not found.')
        
    def test_create_recommender_insufficient_book(self):
        '''
        Simulate a system trying to create user's book recommendation
        but the user did not hav enough book

        An error message should return as response
        '''
        recommender = BookRecommender()

        with self.assertRaises(InsufficientBookError):
            recommender.create_recommend_result(user=self.user2)
        self.assertFalse(os.path.exists(self.path + f'/{self.user2.uid}.txt'),
            'Expected to not created recommend result, but the file is existed.')
        
        library = Library.objects.filter(created_by=self.user2.uid)
        self.assertTrue(library.exists(),
            'Expected library to automatically create, but the library is not found.')
        
        LibraryBook.objects.create(
            library=library[0],
            book=self.book_obj1,
            is_completed=False,
        )

        with self.assertRaises(InsufficientBookError):
            recommender.create_recommend_result(user=self.user2)
        self.assertFalse(os.path.exists(self.path + f'/{self.user2.uid}.txt'),
            'Expected to not created recommend result, but the file is existed.')

class RecommenderListTest(RecommenderAppTestSetUp):

    def test_recommender_list(self):
        '''
        Simulate a user trying to get book recommendation

        Recommended book should return as response
        '''
        self.assertTrue(os.path.exists(self.path + f'/{self.user1.uid}.txt'),
            'Expected recommend result exist, but the file is not found.')
        
        request = self.factory.get(f'/api/recommendation/')
        force_authenticate(request, user=self.user1)
        response = RecommenderViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 1,
            f'Expected only one book as recommend result, not {len(response.data)}.')
        self.assertEqual(response.data[0]['title'], self.book_obj2.title,
            f'Expected response have book with title `{self.book_obj2.title}`.')
        
    def test_recommender_list_no_file(self):
        '''
        Simulate a user trying to get book recommendation
        but user not have a recommendation result in system

        An error message should return as response.
        '''
        request = self.factory.get(f'/api/recommendation/')
        force_authenticate(request, user=self.user2)
        response = RecommenderViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')


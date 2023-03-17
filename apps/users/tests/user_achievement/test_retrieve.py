from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...views import UserAchievementViewSet

class UserAchievementRetrieveTest(UsersAppTestSetUp):

    def test_user_achievement_retrieve(self):
        '''
        Simulate a user trying to retrieve their user_achievement
        by passing :id as path parameter

        A response should return with specific user_achievement data
        '''
        request = self.factory.get(f'/api/user-achievements/{self.user_achievement_obj3}/')
        force_authenticate(request, user=self.user)
        response = UserAchievementViewSet.as_view({'get': 'retrieve'})(request, pk=self.user_achievement_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['achievement_id'], self.achievement_obj1.id,
                         f'Expected `{self.achievement_obj1.id}` as achievement id. not `{response.data["achievement_id"]}`.')

class UserAchievementRetrievePermissionTest(UsersAppTestSetUp):

    def test_user_achievement_retrieve_no_permission(self):
        '''
        Simulate a user trying to retrieve other user's user_achievement
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/user-achievements/{self.user_achievement_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = UserAchievementViewSet.as_view({'get': 'retrieve'})(request, pk=self.user_achievement_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         f'Expected http status 404, not {response.status_code}.')
        
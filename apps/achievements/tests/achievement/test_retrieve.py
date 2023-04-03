from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...views import AchievementViewSet

class AchievementRetrieveTest(AchievementsAppTestSetUp):

    def test_achievement_retrieve(self):
        '''
        Simulate a user trying to retrieve an achievement
        by passing :id as path parameter

        A response should return with specific achievement data
        '''
        request = self.factory.get(f'/api/achievements/{self.achievement_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = AchievementViewSet.as_view({'get': 'retrieve'})(request, pk=self.achievement_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, {response.status_code}.')
        self.assertEqual(response.data['name'], 'test_achievement_1',
                         f'Expected `test_achievement_1` as name, not `{response.data["name"]}`.')
        
class AchievementRetrievePermissionTest(AchievementsAppTestSetUp):

    def test_achievement_retrieve_no_permission(self):
        '''
        Simulate a user trying to retrieve an achievement
        by passing :id as path parameter, but the achievement is not available,
        which is not allowed

        A response should return with specific achievement data
        '''
        request = self.factory.get(f'/api/achievements/{self.achievement_obj2.id}/')
        force_authenticate(request, user=self.user)
        response = AchievementViewSet.as_view({'get': 'retrieve'})(request, pk=self.achievement_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         f'Expected http status 404, {response.status_code}.')
        

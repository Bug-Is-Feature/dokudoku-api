from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...views import AchievementGroupViewSet

class AchievementGroupRetrieveTest(AchievementsAppTestSetUp):

    def test_achievement_group_retrieve(self):
        '''
        Simulate an admin/user trying to retrieve an achievement group
        by passin :id as path parameter

        A response should return with specific achievement_group data
        '''
        request = self.factory.get(f'/api/achievement-groups/{self.achievement_group_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = AchievementGroupViewSet.as_view({'get': 'retrieve'})(request, pk=self.achievement_group_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['name'], self.achievement_group_obj1.name,
                         f'Expected `{self.achievement_group_obj1.name}` as name, not `{response.data["name"]}`.')

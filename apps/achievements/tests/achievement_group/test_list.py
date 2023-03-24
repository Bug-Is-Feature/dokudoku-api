from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import AchievementGroup
from ...serializers import AchievementGroupSerializer
from ...views import AchievementGroupViewSet

class AchievementGroupListTest(AchievementsAppTestSetUp):

    def test_achievement_group_list_view(self):
        '''
        Simulate an admin/user trying to fetch all achievement_groups in the system

        All achievement_groups in the database should return as response
        '''
        request = self.factory.get('/api/achievement-groups/')
        force_authenticate(request, user=self.user)
        response = AchievementGroupViewSet.as_view({'get': 'list'})(request)

        achievement_group = AchievementGroup.objects.all()
        serializers = AchievementGroupSerializer(achievement_group, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
                         'Expected to get all achievement_groups in the database, but the response is not correct.')
        self.assertTrue(len(response.data) == 2,
                        f'Expected 2 achievement_groups from view, not {len(response.data)}.')
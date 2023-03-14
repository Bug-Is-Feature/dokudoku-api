from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import Achievement
from ...serializers import AchievementSerializer
from ...views import AchievementViewSet

class AchievementListTest(AchievementsAppTestSetUp):

    def test_achievement_list_admin_view(self):
        '''
        Simulate an admin trying to fetch all achievements in the system

        All achievement in the database should return as response
        '''
        request = self.factory.get('/api/achievements/')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'get': 'list'})(request)

        achievements = Achievement.objects.all()
        serializers = AchievementSerializer(achievements, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
                         'Expected to get all achievements in the database but the response is not right.')
        self.assertTrue(len(response.data) == 2,
                        f'Expected 2 achievements from view, not {len(response.data)}.')
        
    def test_achievement_list_user_view(self):
        '''
        Simulate a user trying to fetch all achievements in the system

        All achievement in the database that are available should return as response
        '''
        request = self.factory.get('/api/achievements/')
        force_authenticate(request, user=self.user)
        response = AchievementViewSet.as_view({'get': 'list'})(request)

        achievements = Achievement.objects.filter(available=True)
        serializers = AchievementSerializer(achievements, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
                         'Expected to get all achievements in the database but the response is not right.')
        self.assertTrue(len(response.data) == 1,
                        f'Expected 2 achievements from view, not {len(response.data)}.')
from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import UserAchievement
from ...serializers import UserAchievementSerializer
from ...views import UserAchievementViewSet

class UserAchievementTest(UsersAppTestSetUp):

    def test_user_achievement_list_admin_view(self):
        '''
        Simulate an admin trying to fetch every user's achievements in the system

        All user_achievement in the database should show up
        '''
        request = self.factory.get('/api/user-achievements/')
        force_authenticate(request, user=self.admin)
        response = UserAchievementViewSet.as_view({'get': 'list'})(request)

        user_achievements = UserAchievement.objects.all()
        serializers = UserAchievementSerializer(user_achievements, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                        f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
                         'Expected to get every user\'s achievements in database, but the response is not correct.')
        self.assertTrue(len(response.data) == 3,
                        f'Expected 3 user_achievement from admin view, not {len(response.data)}.')
        
    def test_user_achievement_list_user_view(self):
        '''
        Simulate a user trying to fetch their own achievement

        All of their achievement in the database should show up
        '''
        request = self.factory.get('/api/user-achievements/')
        force_authenticate(request, user=self.user)
        response = UserAchievementViewSet.as_view({'get': 'list'})(request)

        user_achievements = UserAchievement.objects.filter(user=request.user.uid)
        serializers = UserAchievementSerializer(user_achievements, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                        f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
                         'Expected to get user\'s achievements in database, but the response is not correct.')
        self.assertTrue(len(response.data) == 1,
                        f'Expected 1 user_achievement from user view, not {len(response.data)}.')
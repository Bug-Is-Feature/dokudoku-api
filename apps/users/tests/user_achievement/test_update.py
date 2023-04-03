from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import UserAchievement
from ...views import UserAchievementViewSet

class UserAchievementUpdateTest(UsersAppTestSetUp):

    def test_user_achievement_update(self):
        '''
        Simulate an admin trying to edit user_achievement

        A response should return with edited user_achievement data
        '''
        request = self.factory.put(f'/api/user-achievements/{self.user_achievement_obj3.id}/', {
            "unlocked_achievement_id": self.achievement_obj2.id
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = UserAchievementViewSet.as_view({'put': 'partial_update'})(request, pk=self.user_achievement_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(UserAchievement.objects.get(id=self.user_achievement_obj3.id).achievement, self.achievement_obj2,
                         f'Expected updated object has achievement with id `{self.achievement_obj2.id}`.')

class UserAchievementUpdatePermissionTest(UsersAppTestSetUp):

    def test_user_achievement_update_no_permission(self):
        '''
        Simulate a user trying to edit user_achievement
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.put(f'/api/user-achievements/{self.user_achievement_obj3.id}/', {
            "unlocked_achievement_id": self.achievement_obj2.id
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserAchievementViewSet.as_view({'put': 'partial_update'})(request, pk=self.user_achievement_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertEqual(UserAchievement.objects.get(id=self.user_achievement_obj3.id).achievement, self.achievement_obj1,
                         f'Expected object has achievement with id `{self.achievement_obj1.id}`, but the value is not correct.')
        
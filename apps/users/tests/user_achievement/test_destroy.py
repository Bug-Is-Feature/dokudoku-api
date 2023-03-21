from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import UserAchievement
from ...views import UserAchievementViewSet

class UserAchievementDestroyTest(UsersAppTestSetUp):

    def test_user_achievement_delete(self):
        '''
        Simulate an admin trying to delete user_achievement

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/user-achievements/{self.user_achievement_obj3.id}/')
        force_authenticate(request, user=self.admin)
        response = UserAchievementViewSet.as_view({'delete': 'destroy'})(request, pk=self.user_achievement_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(UserAchievement.objects.filter(id=self.user_achievement_obj3.id).exists(),
                         f'Expected no user_achievement with id `{self.user_achievement_obj3.id}` still exist.')

class UserAchievementDestroyPermissionTest(UsersAppTestSetUp):

    def test_user_achievement_delete_no_permission(self):
        '''
        Simulate a user trying to delete user_achievement
        which is not allowed

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/user-achievements/{self.user_achievement_obj3.id}/')
        force_authenticate(request, user=self.user)
        response = UserAchievementViewSet.as_view({'delete': 'destroy'})(request, pk=self.user_achievement_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(UserAchievement.objects.filter(id=self.user_achievement_obj3.id).exists(),
                         f'Expected user_achievement with id `{self.user_achievement_obj3.id}` still exist, but thr object got deleted.')
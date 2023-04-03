from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import Achievement
from ...views import AchievementViewSet

class AchievementDestroyTest(AchievementsAppTestSetUp):

    def test_achievement_delete(self):
        '''
        Simulate an admin trying to delete an achievement

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/achievements/{self.achievement_obj2.id}/')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'delete': 'destroy'})(request, pk=self.achievement_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                        f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(Achievement.objects.filter(id=self.achievement_obj2.id).exists(),
                        f'Expected no achievement with id `{self.achievement_obj2.id}` still exist.')
        
class AchievementDestroyPermissionTest(AchievementsAppTestSetUp):

    def test_achievement_delete_no_permission(self):
        '''
        Simulate a user trying to delete an achievement
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/achievements/{self.achievement_obj2.id}/')
        force_authenticate(request, user=self.user)
        response = AchievementViewSet.as_view({'delete': 'destroy'})(request, pk=self.achievement_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                        f'Expected http status 404, not {response.status_code}.')
        self.assertTrue(Achievement.objects.filter(id=self.achievement_obj2.id).exists(),
                        f'Expected achievement with id `{self.achievement_obj2.id}` still exist, but the object got deleted.')
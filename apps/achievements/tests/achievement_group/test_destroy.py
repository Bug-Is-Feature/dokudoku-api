from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import AchievementGroup, Achievement
from ...views import AchievementGroupViewSet

class AchievementGroupDestroyTest(AchievementsAppTestSetUp):

    def test_achievement_group_delete(self):
        '''
        Simulate an admin trying to delete an achievement group

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/achievement-groups/{self.achievement_group_obj2.id}/')
        force_authenticate(request, user=self.admin)
        response = AchievementGroupViewSet.as_view({'delete': 'destroy'})(request, pk=self.achievement_group_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
                         f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(AchievementGroup.objects.filter(id=self.achievement_group_obj2.id).exists(),
                         f'Expected no achievement_group with id `{self.achievement_group_obj2.id}` exist.')

class AchievementGroupDestroyPermissionTest(AchievementsAppTestSetUp):

    def test_achievement_group_delete_no_permission(self):
        '''
        Simulate a user trying to delete an achievement group
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.delete(f'/api/achievement-groups/{self.achievement_group_obj2.id}/')
        force_authenticate(request, user=self.user)
        response = AchievementGroupViewSet.as_view({'delete': 'destroy'})(request, pk=self.achievement_group_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(AchievementGroup.objects.filter(id=self.achievement_group_obj2.id).exists(),
                         f'Expected achievement_group with id `{self.achievement_group_obj2.id}` still exist, but the object got deleted.')
from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import AchievementGroup
from ...views import AchievementGroupViewSet

class AchievementGroupUpdateTest(AchievementsAppTestSetUp):

    def test_achievement_group_update(self):
        '''
        Simulate an admin trying to edit an achievement group

        A response should return with edited achievement_group data
        '''
        request = self.factory.put(f'/api/achievement-groups/{self.achievement_group_obj2.id}/', {
            "name": "edited_achievement_group_name"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementGroupViewSet.as_view({'put': 'partial_update'})(request, pk=self.achievement_group_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(AchievementGroup.objects.get(id=self.achievement_group_obj2.id).name, 'edited_achievement_group_name',
                         'Expected updated data has name = `edited_achievement_group_name`, but the value is not correct.')
    
class AchievementGroupUpdatePermissionTest(AchievementsAppTestSetUp):

    def test_achievement_group_update_no_permissiomn(self):
        '''
        Simulate a user trying to edited achievement group
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.put(f'/api/achievement-groups/{self.achievement_group_obj2.id}/', {
            "name": "edited_achievement_group_name"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = AchievementGroupViewSet.as_view({'put': 'partial_update'})(request, pk=self.achievement_group_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertEqual(AchievementGroup.objects.get(id=self.achievement_group_obj2.id).name, self.achievement_group_obj2.name,
                         f'Expected no change at achievement id: {self.achievement_group_obj2.id}, but the object changed.')
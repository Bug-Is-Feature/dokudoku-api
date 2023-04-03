from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import AchievementGroup
from ...views import AchievementGroupViewSet

class AchievementGroupCreateTest(AchievementsAppTestSetUp):

    def test_achievement_group_create(self):
        '''
        Simulate an admin tryin to create an achievement group

        A response should return with newly created achievement_group data
        '''
        request = self.factory.post('/api/achievement-groups/', {
            "name": "test_achievement_group_3",
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementGroupViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(AchievementGroup.objects.filter(name='test_achievement_group_3').exists(),
                        'Expected `test_achievement_3` existed, but the achievement_group is not found.')
        self.assertTrue(AchievementGroup.objects.count() == 3,
                        'Expected 3 objects found after successfully created.')
        
class AchievementGroupCreatePermissionTest(AchievementsAppTestSetUp):

    def test_achievement_group_create_no_permission(self):
        '''
        Simulate a user trying to create an achievement group
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.post('/api/achievement-groups/', {
            "name": "test_achievement_group_3",
        }, format='json')
        force_authenticate(request, user=self.user)
        response = AchievementGroupViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                         f'Expected http status 403, not {response.status_code}.')
        self.assertFalse(AchievementGroup.objects.filter(name='test_achievement_group_3').exists(),
                        'Expected no achievement group with name`test_achievement_3`, but the achievement_group created with no permission.')
        self.assertTrue(AchievementGroup.objects.count() == 2,
                        'Expected only 2 objects existed in the system.')
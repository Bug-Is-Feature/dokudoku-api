from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import Achievement
from ...views import AchievementViewSet

class AchievementCreateTest(AchievementsAppTestSetUp):

    def test_achievement_create(self):
        '''
        Simulate an admin trying to create an achievement

        A response should return with newly created achievement data
        '''
        request = self.factory.post('/api/achievements/', {
            "name": "test_achievement_3",
            "description": "test_test",
            "group_id": self.achievement_group_obj1.id,
            "locked_thumbnail": "test_locked_thumbnail",
            "unlocked_thumbnail": "test_unlocked_thumbnail",
            "condition": Achievement.UnlockCondition.HOURGLASS_READING_HOUR.label,
            "threshold": 30,
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                        f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(Achievement.objects.filter(name='test_achievement_3').exists(),
                        'Expected `test_achievement_3` existed, but the achievement is not found.')
        self.assertTrue(Achievement.objects.count() == 3,
                        'Expected 3 objects found after successfully created.')
        self.assertEqual(response.data['group']['name'], self.achievement_group_obj1.name,
                         f'Expected response group name = `{self.achievement_group_obj1.name}`, but the value is not correct.')

class AchievementCreatePermissionTest(AchievementsAppTestSetUp):

    def test_achievement_create_no_permission(self):
        '''
        Simulate a user trying to create an achievement
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.post('/api/achievements/', {
            "name": "test_achievement_4",
            "description": "test_test",
            "locked_thumbnail": "test_locked_thumbnail",
            "unlocked_thumbnail": "test_unlocked_thumbnail",
            "condition": Achievement.UnlockCondition.STOPWATCH_READING_HOUR.label,
            "threshold": 30,
        }, format='json')
        force_authenticate(request, user=self.user)
        response = AchievementViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                        f'Expected http status 403, not {response.status_code}.')
        self.assertFalse(Achievement.objects.filter(name='test_achievement_4').exists(),
                        'Expected no achievement with name `test_achievement_3`, but the achievement created with out permission.')
        self.assertTrue(Achievement.objects.count() == 2,
                        'Expected only 2 objects existed in the system.')
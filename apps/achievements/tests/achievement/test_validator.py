from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import Achievement
from ...views import AchievementViewSet

class AchievementThresholdValidatorTest(AchievementsAppTestSetUp):

    def test_achievement_validator_invalid_threshold_type(self):
        '''
        Simulate an admin trying to create an achievement
        but passing invalid threshold as attribute (not int)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/achievements/', {
            "name": "test_achievement",
            "description": "test_test",
            "condition": Achievement.UnlockCondition.HOURGLASS_READING_HOUR.label,
            "threshold": 30.05,
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertTrue(Achievement.objects.count() == 2,
            'Expected no achievement created.')

    def test_achievement_validator_negative_threshold_type(self):
        '''
        Simulate an admin trying to create an achievement
        but passing invalid threshold as attribute (negative int)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/sessions/', {
            "name": "test_achievement",
            "description": "test_test",
            "condition": Achievement.UnlockCondition.HOURGLASS_READING_HOUR.label,
            "threshold": -30,
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertTrue(Achievement.objects.count() == 2,
            'Expected no achievement created.')
        
class AchievementConditionValidatorTest(AchievementsAppTestSetUp):
        
    def test_achievement_validator_invalid_condition_type(self):
        '''
        Simulate an admin trying to create an achievement
        but passing invalid timer_type as attribute (not match with enum)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/sessions/', {
            "name": "test_achievement",
            "description": "test_test",
            "condition": "X",
            "threshold": 30,
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertTrue(Achievement.objects.count() == 2,
            'Expected no achievement created.')
        
class AchievementAvailableValidatorTest(AchievementsAppTestSetUp):

    def test_achievement_validator_invalid_available_type(self):
        '''
        Simulate an admin trying to create an achievement
        but passing invalid timer_type as attribute (not match with enum)
        
        An error message should return as response
        '''
        request = self.factory.post('/api/sessions/', {
            "name": "test_achievement",
            "description": "test_test",
            "condition": Achievement.UnlockCondition.STOPWATCH_READING_HOUR,
            "available": "not_bool",
            "threshold": 30,
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST,
            f'Expected http status 400, not {response.status_code}.')
        self.assertTrue(Achievement.objects.count() == 2,
            'Expected no achievement created.')

        
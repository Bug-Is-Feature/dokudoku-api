from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import AchievementsAppTestSetUp
from ...models import Achievement
from ...views import AchievementViewSet

class AchievementUpdateTest(AchievementsAppTestSetUp):

    def test_achievement_update(self):
        '''
        Simulate an admin trying to edit an achievement

        A response should return with edited achievement data
        '''
        request = self.factory.put(f'/api/achievements/{self.achievement_obj2.id}/', {
            "name": "test_update"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'put': 'partial_update'})(request, pk=self.achievement_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(Achievement.objects.get(id=self.achievement_obj2.id).name, 'test_update',
                        'Expected updated data has name = `test_update`, but the value is not right.')
        
    def test_achievement_available_update(self):
        '''
        Simulate an admin trying to edit an achievement `available` attribute

        A response should return with edited achievement data
        '''
        request = self.factory.put(f'/api/achievements/{self.achievement_obj2.id}/', {
            "available": True
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AchievementViewSet.as_view({'put': 'partial_update'})(request, pk=self.achievement_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(Achievement.objects.get(id=self.achievement_obj2.id).available,
                        'Expected updated data has available = `true`, but the value is not right.')
        
class AchievementUpdatePermissionTest(AchievementsAppTestSetUp):
    
    def test_achievement_update_no_permission(self):
        '''
        Simulate a user trying to edit an achievement
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.put(f'/api/achievements/{self.achievement_obj2.id}/', {
            "name": "test_update"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = AchievementViewSet.as_view({'put': 'partial_update'})(request, pk=self.achievement_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
                         f'Expected http status 404, not {response.status_code}.')
        self.assertEqual(Achievement.objects.get(id=self.achievement_obj2.id).name, 'test_achievement_2',
                        f'Expected no change at achievement id: {self.achievement_obj2.id}, but the object changed.')

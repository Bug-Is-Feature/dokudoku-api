from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import UsersAppTestSetUp
from ...models import UserAchievement
from ...views import UserAchievementViewSet

class UserAchievementCreateTest(UsersAppTestSetUp):

    def test_user_achievement_create(self):
        '''
        Simulate a user trying to create an user_achievement

        A response should return with newly create user_achievement
        '''
        request = self.factory.post('/api/user-achievements/', {
            "uid": self.user.uid,
            "unlocked_achievement_id": self.achievement_obj2.id,
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserAchievementViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         f'Expected http status 201, not {response.status_code}.')
        self.assertTrue(UserAchievement.objects.count() == 4,
                        f'Expected total 4 user_achievements items after created, not {UserAchievement.objects.count()}.')
        self.assertTrue(UserAchievement.objects.filter(user=self.user.uid, achievement=self.achievement_obj2.id).exists(),
                        'Expected newly created object exist, but the object is not found.')

class UserAchievementCreatePermissionTest(UsersAppTestSetUp):

    def test_user_achievement_create_no_permission(self):
        '''
        Simulate a user trying to create an user_achievement
        but passing other user uid as attribute

        An error message should return as response
        '''
        request = self.factory.post('/api/user-achievements/', {
            "uid": self.admin.uid,
            "unlocked_achievement_id": self.achievement_obj2.id,
        }, format='json')
        force_authenticate(request, user=self.user)
        response = UserAchievementViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
                        f'Expected http status 403, not {response.status_code}.')
        self.assertTrue(UserAchievement.objects.count() == 3,
                        f'Expected only 3 user_achievement exist, not {UserAchievement.objects.count()}.')
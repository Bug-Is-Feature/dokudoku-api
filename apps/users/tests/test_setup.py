import uuid

from rest_framework.test import APITestCase, APIRequestFactory

from apps.achievements.models import Achievement
from ..models import User, UserAchievement

class UsersAppTestSetUp(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin@admin.com'
        )
        self.user = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user@user.com',
        )
        self.achievement_obj1 = Achievement.objects.create(
            name='test_achievement_1',
            description='test_desc',
            condition=Achievement.UnlockCondition.TOTAL_READING_HOUR,
            threshold=24,
            available=True,
        )
        self.achievement_obj2 = Achievement.objects.create(
            name='test_achievement_2',
            description='test_desc',
            condition=Achievement.UnlockCondition.BOOK_AMOUNT,
            threshold=20,
            available=False,
        )
        self.user_achievement_obj1 = UserAchievement.objects.create(
            user=self.admin,
            achievement=self.achievement_obj1,
        )
        self.user_achievement_obj2 = UserAchievement.objects.create(
            user=self.admin,
            achievement=self.achievement_obj2,
        )
        self.user_achievement_obj3 = UserAchievement.objects.create(
            user=self.user,
            achievement=self.achievement_obj1,
        )
            
import uuid

from rest_framework.test import APITestCase, APIRequestFactory

from apps.users.models import User
from ..models import Achievement, AchievementGroup

class AchievementsAppTestSetUp(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin@admin.com',
        )
        self.user = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user@user.com',
        )
        self.achievement_group_obj1 = AchievementGroup.objects.create(
            name='test_achievement_group_1',
        )
        self.achievement_group_obj2 = AchievementGroup.objects.create(
            name='test_achievement_group_2',
        )
        self.achievement_obj1 = Achievement.objects.create(
            name='test_achievement_1',
            description='test_desc',
            group=self.achievement_group_obj1,
            locked_thumbnail='test_locked_thumbnail',
            unlocked_thumbnail='test_unlocked_thumbnail',
            condition=Achievement.UnlockCondition.TOTAL_READING_HOUR,
            threshold=24,
            available=True,
        )
        self.achievement_obj2 = Achievement.objects.create(
            name='test_achievement_2',
            description='test_desc',
            group=self.achievement_group_obj2,
            locked_thumbnail='test_locked_thumbnail',
            unlocked_thumbnail='test_unlocked_thumbnail',
            condition=Achievement.UnlockCondition.BOOK_AMOUNT,
            threshold=20,
            available=False,
        )
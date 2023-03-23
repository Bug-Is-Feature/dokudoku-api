from rest_framework import serializers

from apps.achievements.serializers import AchievementSerializer
from .models import User, UserAchievement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('date_joined',)

class UserAchievementSerializer(serializers.ModelSerializer):
    user_achievement_id = serializers.IntegerField(source='id', read_only=True)
    # achievement = AchievementSerializer(many=False, read_only=True)
    achievement_id = serializers.IntegerField(source='achievement.id', read_only=True)

    class Meta:
        model = UserAchievement
        fields = ('user_achievement_id', 'uid', 'unlocked_achievement_id', 'achievement_id',)
        extra_kwargs = {
            'uid': {'source': 'user', 'write_only': True},
            'unlocked_achievement_id': {'source': 'achievement', 'write_only': True},
        }

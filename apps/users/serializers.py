from django.conf import settings
from django.http import JsonResponse
from firebase_admin import auth
from rest_framework import serializers

from .models import User, UserAchievement

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
        read_only_fields = ('date_joined',)

class UserAchievementSerializer(serializers.ModelSerializer):
    user_achievement_id = serializers.IntegerField(source='id', read_only=True)
    achievement_id = serializers.IntegerField(source='achievement.id', read_only=True)

    class Meta:
        model = UserAchievement
        fields = ('user_achievement_id', 'uid', 'unlocked_achievement_id', 'achievement_id',)
        extra_kwargs = {
            'uid': {'source': 'user', 'write_only': True},
            'unlocked_achievement_id': {'source': 'achievement', 'write_only': True},
        }

class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'email', 'last_login', 'is_admin', 'date_joined',)
        read_only_fields = ('date_joined',)

    def update(self, instance, validated_data):
        if not settings.DEBUG:
            update_status = validated_data.get('is_admin')
            if update_status == True:
                try:
                    auth.set_custom_user_claims(instance.uid, {
                        'isAdmin': True,
                    })
                except:
                    return JsonResponse(
                        'Firebase service unavailable, can\'t create custom user claims.', status=503)
            elif update_status == False:
                try:
                    auth.set_custom_user_claims(instance.uid, None)
                except:
                    return JsonResponse(
                        'Firebase service unavailable, can\'t create custom user claims.', status=503)
        return super().update(instance, validated_data)

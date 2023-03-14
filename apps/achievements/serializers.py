from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from apps.utils.serializers import ChoiceField
from .models import Achievement

class AchievementSerializer(serializers.ModelSerializer):
    condition = ChoiceField(choices=Achievement.UnlockCondition.choices)

    class Meta:
        model = Achievement
        exclude = ('created_at',)
        extra_kwargs = {
            'available': {'write_only': True},
        }

    def create(self, validated_data):
        if self.context['request'].user.is_admin:
            return Achievement.objects.create(**validated_data)
        else:
            raise PermissionDenied
        
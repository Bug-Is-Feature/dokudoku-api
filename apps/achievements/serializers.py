from django.core.exceptions import PermissionDenied
from rest_framework import serializers

from apps.utils.serializers import ChoiceField
from .models import Achievement, AchievementGroup

class AchievementGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AchievementGroup
        fields = ('__all__')

class AchievementSerializer(serializers.ModelSerializer):
    condition = ChoiceField(choices=Achievement.UnlockCondition.choices)
    group = AchievementGroupSerializer(many=False, read_only=True)

    class Meta:
        model = Achievement
        fields = (
            'name', 'description', 'locked_thumbnail', 'unlocked_thumbnail',
            'condition', 'threshold', 'available', 'group', 'group_id',
        )
        extra_kwargs = {
            'available': {'write_only': True},
            'group_id': {'source': 'group', 'write_only': True}
        }

    def create(self, validated_data):
        if self.context['request'].user.is_admin:
            return Achievement.objects.create(**validated_data)
        else:
            raise PermissionDenied
        
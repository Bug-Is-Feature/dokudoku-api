from rest_framework import viewsets

from .models import Achievement, AchievementGroup
from .serializers import AchievementSerializer, AchievementGroupSerializer
from .permissions import AchievementPermission, AchievementGroupPermission

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = (AchievementPermission,)

    def get_queryset(self):
        if self.request.user.is_admin:
            return Achievement.objects.all()
        else:
            return Achievement.objects.filter(available=True)
        
class AchievementGroupViewSet(viewsets.ModelViewSet):
    queryset = AchievementGroup.objects.all()
    serializer_class = AchievementGroupSerializer
    permission_classes = (AchievementGroupPermission,)

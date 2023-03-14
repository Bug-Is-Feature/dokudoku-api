from rest_framework import viewsets

from .models import Achievement
from .serializers import AchievementSerializer
from .permissions import AchievementPermission

class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = (AchievementPermission,)

    def get_queryset(self):
        if self.request.user.is_admin:
            return Achievement.objects.all()
        else:
            return Achievement.objects.filter(available=True)

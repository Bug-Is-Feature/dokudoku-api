from rest_framework import viewsets

from .models import User, UserAchievement
from .serializers import UserSerializer, UserAchievementSerializer
from .permissions import UserPermission, UserAchievementPermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

class UserAchievementViewSet(viewsets.ModelViewSet):
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer
    permission_classes = (UserAchievementPermission,)

    def get_queryset(self):
        if self.request.user.is_admin:
            return UserAchievement.objects.all()
        else:
            return UserAchievement.objects.filter(user=self.request.user)